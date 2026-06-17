"""
Planner agent — decomposes a user request into an ordered list of
sub-tasks and returns structured JSON.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

from prompts.planner_prompt import PLANNER_SYSTEM_PROMPT
from utils.gemini_client import get_chat_llm
from utils.helpers import call_gemini_json

logger = logging.getLogger(__name__)


def plan(user_task: str) -> Dict[str, Any]:
    """Break *user_task* into an ordered list of sub-tasks.

    Returns
    -------
    dict
        ``{"goal": str, "tasks": [str, ...]}``
        On failure: ``{"error": str, ...}``
    """
    logger.info("Planner called with task: '%s'", user_task)

    llm = get_chat_llm(temperature=0.2)
    user_content = f"User task:\n{user_task}"

    result = call_gemini_json(
        llm=llm,
        system_prompt=PLANNER_SYSTEM_PROMPT,
        user_content=user_content,
        fallback={
            "goal": user_task,
            "tasks": [
                "Retrieve relevant policies",
                "Identify required documents",
                "Generate checklist",
                "Verify compliance",
            ],
            "_fallback": True,
        },
    )

    logger.info(
        "Planner produced %d task(s) for goal '%s'.",
        len(result.get("tasks", [])),
        result.get("goal", "?"),
    )
    return result
