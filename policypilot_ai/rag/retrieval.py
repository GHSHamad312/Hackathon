"""
Retrieval interface for PolicyPilot AI.

Exposes a single ``retrieve()`` function that returns plain
dictionaries (not raw LangChain objects) so any agent in the
pipeline can consume results without importing LangChain.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any

from rag.vectorstore import load_vectorstore

logger = logging.getLogger(__name__)


# ── Public API ───────────────────────────────────────────────────────

def retrieve(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """Return the top-*k* chunks most relevant to *query*.

    Each result is a plain dictionary with keys:

    - ``text``   — the chunk content.
    - ``source`` — the originating PDF filename.
    - ``page``   — the page number within that PDF.
    - ``score``  — the similarity score (lower = more similar for L2).

    Returns an empty list if no vector store has been built yet.
    """
    db = load_vectorstore()
    if db is None:
        logger.warning("retrieve() called but no FAISS index exists yet.")
        return []

    # similarity_search_with_score returns List[Tuple[Document, float]]
    try:
        raw_results = db.similarity_search_with_score(query, k=k)
    except Exception as exc:
        logger.error("FAISS similarity search failed: %s", exc)
        return []

    results: List[Dict[str, Any]] = []
    for doc, score in raw_results:
        results.append({
            "text": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "page": doc.metadata.get("page", 0),
            "score": float(score),
        })

    logger.info(
        "Retrieved %d chunk(s) for query '%.60s…'",
        len(results),
        query,
    )
    return results


def format_context(results: List[Dict[str, Any]]) -> str:
    """Format retrieval results into a single context string for the LLM.

    Parameters
    ----------
    results : list[dict]
        Output of ``retrieve()``.

    Returns
    -------
    str
        A newline-separated block of text with source citations.
    """
    if not results:
        return "(No relevant documents found.)"

    parts: List[str] = []
    for i, r in enumerate(results, 1):
        header = f"[Source {i}: {r['source']}, p.{r['page']}]"
        parts.append(f"{header}\n{r['text']}")

    return "\n\n---\n\n".join(parts)
