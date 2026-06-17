"""
Retriever agent — thin wrapper that runs retrieval for each planner
task, deduplicates results, and returns a combined list of passages.

This agent does NOT call Gemini — it only queries the FAISS vector store.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from rag.retrieval import retrieve

logger = logging.getLogger(__name__)


def retrieve_for_tasks(tasks: List[str], k: int = 4) -> List[Dict[str, Any]]:
    """Retrieve relevant passages for each task in *tasks*.

    Parameters
    ----------
    tasks : list[str]
        Sub-tasks from the planner (e.g. "retrieve HR policy").
    k : int
        Number of results per task query.

    Returns
    -------
    list[dict]
        Deduplicated list of passage dicts, each with keys
        ``text``, ``source``, ``page``, ``score``.
    """
    if not tasks:
        logger.warning("retrieve_for_tasks called with empty task list.")
        return []

    seen_texts: set = set()
    combined: List[Dict[str, Any]] = []

    for task in tasks:
        logger.info("Retrieving for task: '%s'", task)
        results = retrieve(task, k=k)

        for r in results:
            # Deduplicate by text content (use first 200 chars as key)
            dedup_key = r["text"][:200]
            if dedup_key not in seen_texts:
                seen_texts.add(dedup_key)
                combined.append(r)

    logger.info(
        "Retrieved %d unique passage(s) across %d task(s).",
        len(combined), len(tasks),
    )
    return combined
