from __future__ import annotations

import logging
from typing import Any, Dict

from prompts.action_prompt import ACTION_SYSTEM_PROMPT, build_action_user_prompt
from utils.gemini_client import get_chat_llm
from utils.helpers import call_gemini_json, now_iso

logger = logging.getLogger(__name__)


def simulate_actions(generated_docs: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate downstream enterprise actions dynamically.

    Parameters
    ----------
    generated_docs : dict
        Output of ``generator.generate_documents()``.

    Returns
    -------
    dict
        Status object with simulated action results.
    """
    logger.info("Action agent determining downstream actions dynamically …")

    llm = get_chat_llm(temperature=0.1)
    user_content = build_action_user_prompt(generated_docs)

    result = call_gemini_json(
        llm=llm,
        system_prompt=ACTION_SYSTEM_PROMPT,
        user_content=user_content,
        fallback={
            "generic_ticket": "created",
            "pdf_generation": "ready"
        },
    )

    result["timestamp"] = now_iso()
    result["pdf_download"] = "ready" # Always include this as standard

    created_count = sum(1 for v in result.values() if isinstance(v, str) and v.lower() in ["created", "ready", "submitted", "sent"])
    logger.info("Action agent triggered %d dynamic actions.", created_count)
    
    return result
