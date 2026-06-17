"""
Compliance agent — checks reasoning output against policy passages
for missing requirements or violations.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from prompts.compliance_prompt import COMPLIANCE_SYSTEM_PROMPT
from utils.gemini_client import get_chat_llm
from utils.helpers import call_gemini_json

logger = logging.getLogger(__name__)


def check_compliance(
    reasoning_output: Dict[str, Any],
    retrieved_passages: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Check *reasoning_output* against policy *passages*.

    Returns
    -------
    dict
        ``{"compliance_score", "missing_requirements",
          "warnings", "recommendations"}``
        On failure: ``{"error": str, ...}``
    """
    logger.info("Compliance agent checking reasoning output …")

    # ── Build the user content ───────────────────────────────────────
    from prompts.compliance_prompt import build_compliance_user_prompt
    user_content = build_compliance_user_prompt(
        reasoning_output=reasoning_output,
        retrieved_passages=retrieved_passages,
    )

    llm = get_chat_llm(temperature=0.1)

    result = call_gemini_json(
        llm=llm,
        system_prompt=COMPLIANCE_SYSTEM_PROMPT,
        user_content=user_content,
        fallback={
            "compliance_score": 0,
            "missing_requirements": ["Unable to perform compliance check."],
            "warnings": ["Compliance agent encountered a parsing error."],
            "recommendations": ["Please review manually."],
            "_fallback": True,
        },
    )

    logger.info(
        "Compliance score: %s, %d warning(s), %d missing req(s).",
        result.get("compliance_score", "?"),
        len(result.get("warnings", [])),
        len(result.get("missing_requirements", [])),
    )
    return result


def _format_passages(passages: List[Dict[str, Any]]) -> str:
    """Format retrieved passages into a numbered text block."""
    if not passages:
        return "(No policy passages available.)"
    parts = []
    for i, p in enumerate(passages, 1):
        source = p.get("source", "unknown")
        page = p.get("page", "?")
        parts.append(f"[Policy {i} — {source}, p.{page}]\n{p['text']}")
    return "\n\n---\n\n".join(parts)
