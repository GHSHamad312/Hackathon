"""
Miscellaneous helper functions used across the project.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import textwrap
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def truncate(text: str, max_chars: int = 500) -> str:
    """Return *text* truncated to *max_chars* with an ellipsis."""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1] + "…"


def md5_hash(text: str) -> str:
    """Quick deterministic hash — useful for dedup / cache keys."""
    return hashlib.md5(text.encode()).hexdigest()


def now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def dedent(text: str) -> str:
    """Convenience wrapper around textwrap.dedent + strip."""
    return textwrap.dedent(text).strip()


# ── Defensive JSON parsing for LLM responses ────────────────────────

_FENCE_RE = re.compile(
    r"```(?:json)?\s*\n?(.*?)\n?\s*```",
    re.DOTALL,
)


def strip_json_fences(text: str) -> str:
    """Remove markdown code fences (```json ... ```) from *text*."""
    match = _FENCE_RE.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()


def safe_parse_json(
    raw: str,
    fallback: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Parse a JSON string defensively.

    1. Strip markdown code fences if present.
    2. Attempt ``json.loads``.
    3. On failure return *fallback* (defaults to an error dict).
    """
    cleaned = strip_json_fences(raw)
    try:
        return json.loads(cleaned)
    except (json.JSONDecodeError, TypeError) as exc:
        logger.warning("JSON parse failed: %s — raw[:200]=%s", exc, cleaned[:200])
        if fallback is not None:
            return fallback
        return {"error": f"JSON parse failed: {exc}", "raw_response": cleaned[:500]}


def call_gemini_json(
    llm,
    system_prompt: str,
    user_content: str,
    fallback: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Call Gemini with a system+user prompt and parse the JSON response.

    Implements the retry-on-parse-failure strategy:
      1. Send the initial request.
      2. If the response isn't valid JSON, retry once with a stricter
         "return only JSON, no explanation" reminder.
      3. If still invalid, return *fallback* or an error dict.
    """
    from langchain_core.messages import HumanMessage, SystemMessage

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content),
    ]

    # ── First attempt ────────────────────────────────────────────────
    try:
        response = llm.invoke(messages)
        raw = response.content
    except Exception as exc:
        logger.error("Gemini call failed: %s", exc)
        err = {"error": f"Gemini API error: {exc}"}
        return fallback if fallback is not None else err

    result = _try_parse(raw)
    if result is not None:
        return result

    # ── Retry with stricter instruction ──────────────────────────────
    logger.info("First JSON parse failed — retrying with stricter prompt.")
    retry_messages = messages + [
        HumanMessage(
            content=(
                "Your previous response was not valid JSON. "
                "Please respond with ONLY the raw JSON object — "
                "no markdown fences, no explanation, no extra text."
            ),
        ),
    ]
    try:
        response = llm.invoke(retry_messages)
        raw = response.content
    except Exception as exc:
        logger.error("Gemini retry call failed: %s", exc)
        err = {"error": f"Gemini API retry error: {exc}"}
        return fallback if fallback is not None else err

    result = _try_parse(raw)
    if result is not None:
        return result

    # ── Both attempts failed ─────────────────────────────────────────
    logger.error("JSON parse failed after retry. raw[:300]=%s", raw[:300])
    if fallback is not None:
        return fallback
    return {"error": "Failed to parse JSON after retry", "raw_response": raw[:500]}


def _try_parse(raw: str) -> Optional[Dict[str, Any]]:
    """Attempt to parse *raw* as JSON, return None on failure."""
    cleaned = strip_json_fences(raw)
    try:
        return json.loads(cleaned)
    except (json.JSONDecodeError, TypeError):
        return None
