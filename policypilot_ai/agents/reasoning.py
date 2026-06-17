"""
Reasoning agent — synthesises retrieved passages and the planner's
task list into a structured analysis.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from prompts.reasoning_prompt import REASONING_SYSTEM_PROMPT
from utils.gemini_client import get_chat_llm
from utils.helpers import call_gemini_json

logger = logging.getLogger(__name__)


def reason(
    user_task: str,
    retrieved_passages: List[Dict[str, Any]],
    plan: Dict[str, Any],
) -> Dict[str, Any]:
    """Analyse passages and plan to produce a structured reasoning output.

    Returns
    -------
    dict
        ``{"summary", "required_documents", "actions",
          "departments", "dependencies"}``
        On failure: ``{"error": str, ...}``
    """
    logger.info("Reasoning agent called for task: '%s'", user_task)

    # ── Build the user content ───────────────────────────────────────
    passages_text = _format_passages(retrieved_passages)
    tasks_text = json.dumps(plan.get("tasks", []), indent=2)

    user_content = (
        f"User's original request:\n{user_task}\n\n"
        f"Planner's task list:\n{tasks_text}\n\n"
        f"Retrieved document passages:\n{passages_text}"
    )

    llm = get_chat_llm(temperature=0.3)

    result = call_gemini_json(
        llm=llm,
        system_prompt=REASONING_SYSTEM_PROMPT,
        user_content=user_content,
        fallback={
            "summary": f"Analysis for: {user_task}",
            "required_documents": [],
            "actions": plan.get("tasks", []),
            "departments": ["HR"],
            "dependencies": [],
            "_fallback": True,
        },
    )

    logger.info(
        "Reasoning produced %d action(s), %d required doc(s).",
        len(result.get("actions", [])),
        len(result.get("required_documents", [])),
    )
    return result


def _format_passages(passages: List[Dict[str, Any]]) -> str:
    """Format retrieved passages into a numbered text block."""
    if not passages:
        return "(No passages retrieved.)"
    parts = []
    for i, p in enumerate(passages, 1):
        source = p.get("source", "unknown")
        page = p.get("page", "?")
        parts.append(f"[Passage {i} — {source}, p.{page}]\n{p['text']}")
    return "\n\n---\n\n".join(parts)
