"""
PDF ingestion pipeline for PolicyPilot AI.

Accepts uploaded PDF file-like objects (from Streamlit's file_uploader),
extracts text page-by-page with pypdf, splits into overlapping chunks
using LangChain's RecursiveCharacterTextSplitter, and returns a list of
LangChain Document objects enriched with source metadata.

Edge cases handled:
  - No files provided             → returns ([], "No PDF files provided.")
  - Empty PDF (zero pages)        → skipped with warning
  - Unreadable / scanned PDF      → skipped with warning
"""

from __future__ import annotations

import logging
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, List, Tuple, Union

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

logger = logging.getLogger(__name__)

# Type alias: Streamlit's UploadedFile behaves like a BinaryIO with a
# `.name` attribute, but we also accept raw paths for CLI / testing.
FileInput = Union[BinaryIO, Path, str]


# ── Public API ───────────────────────────────────────────────────────

def ingest_pdfs(
    files: List[FileInput],
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> Tuple[List[Document], List[str]]:
    """Ingest one or more PDF files and return chunked Documents.

    Parameters
    ----------
    files : list
        File-like objects (e.g. from ``st.file_uploader``) or file paths.
    chunk_size : int
        Target chunk size in characters (≈ tokens for English).
    chunk_overlap : int
        Number of overlapping characters between consecutive chunks.

    Returns
    -------
    (documents, warnings) : tuple
        *documents* is a flat list of :class:`Document` chunks.
        *warnings* collects human-readable messages for any files that
        were skipped (empty, unreadable, etc.).
    """
    if not files:
        return [], ["No PDF files provided."]

    all_docs: List[Document] = []
    warnings: List[str] = []

    for file in files:
        filename, page_docs, file_warnings = _extract_single_pdf(file)
        warnings.extend(file_warnings)
        if page_docs:
            all_docs.extend(page_docs)
            logger.info("Extracted %d page(s) from '%s'.", len(page_docs), filename)
        else:
            msg = f"'{filename}': no extractable text (possibly scanned/image-only)."
            warnings.append(msg)
            logger.warning(msg)

    if not all_docs:
        warnings.append("No text could be extracted from any of the uploaded PDFs.")
        return [], warnings

    # ── Chunking ─────────────────────────────────────────────────────
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(all_docs)
    logger.info(
        "Split %d page-document(s) into %d chunks (size=%d, overlap=%d).",
        len(all_docs), len(chunks), chunk_size, chunk_overlap,
    )
    return chunks, warnings


# ── Internals ────────────────────────────────────────────────────────

def _extract_single_pdf(
    file: FileInput,
) -> Tuple[str, List[Document], List[str]]:
    """Extract per-page Documents from a single PDF.

    Returns ``(filename, documents, warnings)``.
    """
    warnings: List[str] = []

    # Resolve filename + reader
    try:
        if isinstance(file, (str, Path)):
            path = Path(file)
            filename = path.name
            reader = PdfReader(str(path))
        else:
            # file-like object (Streamlit UploadedFile)
            filename = getattr(file, "name", "unknown.pdf")
            file.seek(0)  # ensure we read from the beginning
            reader = PdfReader(BytesIO(file.read()))
    except Exception as exc:
        msg = f"'{getattr(file, 'name', file)}': could not read PDF — {exc}"
        logger.error(msg)
        return (getattr(file, "name", "unknown.pdf"), [], [msg])

    if len(reader.pages) == 0:
        msg = f"'{filename}': PDF has zero pages."
        warnings.append(msg)
        logger.warning(msg)
        return (filename, [], warnings)

    docs: List[Document] = []
    for page_num, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            msg = f"'{filename}' page {page_num}: extraction error — {exc}"
            warnings.append(msg)
            logger.warning(msg)
            continue

        text = text.strip()
        if not text:
            continue

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source": filename,
                    "page": page_num,
                },
            )
        )

    return (filename, docs, warnings)
