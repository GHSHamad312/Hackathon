"""
FAISS vector-store management for PolicyPilot AI.

Builds, saves, loads, and queries a FAISS index using Google Gemini
embeddings (via GoogleGenerativeAIEmbeddings from langchain-google-genai).

The index is persisted inside ``config.VECTORSTORE_DIR`` so it survives
Streamlit reruns within a session.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from config import VECTORSTORE_DIR
from utils.gemini_client import get_embeddings

logger = logging.getLogger(__name__)

_FAISS_INDEX_NAME = "policypilot_index"


# ── Public API ───────────────────────────────────────────────────────

def index_exists() -> bool:
    """Return True if a persisted FAISS index is on disk."""
    faiss_file = VECTORSTORE_DIR / f"{_FAISS_INDEX_NAME}.faiss"
    pkl_file = VECTORSTORE_DIR / f"{_FAISS_INDEX_NAME}.pkl"
    exists = faiss_file.exists() and pkl_file.exists()
    logger.debug("Index exists check: %s (faiss=%s, pkl=%s)", exists, faiss_file, pkl_file)
    return exists


def build_vectorstore(documents: List[Document]) -> FAISS:
    """Create a FAISS index from chunked Documents, persist, and return it.

    Parameters
    ----------
    documents : list[Document]
        Chunked documents (output of ``ingest.ingest_pdfs``).

    Returns
    -------
    FAISS
        The built vector store, ready for similarity search.

    Raises
    ------
    ValueError
        If *documents* is empty.
    RuntimeError
        If the API key is missing (raised by ``get_embeddings``).
    """
    if not documents:
        raise ValueError("Cannot build a vector store from zero documents.")

    logger.info("Building FAISS index from %d chunks …", len(documents))
    embeddings = get_embeddings()

    # FAISS.from_documents handles batching internally
    db = FAISS.from_documents(documents, embeddings)

    # Persist to disk
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    db.save_local(str(VECTORSTORE_DIR), index_name=_FAISS_INDEX_NAME)
    logger.info(
        "FAISS index saved to %s (%d vectors).",
        VECTORSTORE_DIR, len(documents),
    )
    return db


def load_vectorstore() -> Optional[FAISS]:
    """Load a previously-persisted FAISS index, or return ``None``.

    Returns
    -------
    FAISS | None
        The loaded vector store, or ``None`` if no index exists on disk.
    """
    if not index_exists():
        logger.info("No existing FAISS index found at %s.", VECTORSTORE_DIR)
        return None

    logger.info("Loading FAISS index from %s …", VECTORSTORE_DIR)
    embeddings = get_embeddings()
    db = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        index_name=_FAISS_INDEX_NAME,
        allow_dangerous_deserialization=True,
    )
    logger.info("FAISS index loaded successfully.")
    return db


def get_or_build_vectorstore(
    documents: Optional[List[Document]] = None,
) -> Optional[FAISS]:
    """Load an existing index if available; otherwise build from *documents*.

    Convenience wrapper used by the retrieval layer and the Streamlit UI
    to avoid redundant rebuilds across reruns.

    Parameters
    ----------
    documents : list[Document] | None
        If no saved index exists and *documents* is provided, a new
        index is built and persisted.  If *documents* is ``None`` and
        no saved index exists, returns ``None``.
    """
    db = load_vectorstore()
    if db is not None:
        return db

    if documents:
        return build_vectorstore(documents)

    logger.warning("No index on disk and no documents supplied — returning None.")
    return None


def clear_vectorstore() -> None:
    """Delete persisted index files (useful for re-indexing)."""
    for suffix in (".faiss", ".pkl"):
        path = VECTORSTORE_DIR / f"{_FAISS_INDEX_NAME}{suffix}"
        if path.exists():
            path.unlink()
            logger.info("Deleted %s.", path)
