"""
End-to-end smoke test for the RAG pipeline.

Creates a dummy PDF with realistic HR policy text, runs it through
ingest → vectorstore → retrieval and verifies each step.
"""

import sys
import logging
from io import BytesIO
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

logging.basicConfig(level=logging.INFO, format="%(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger("test_rag")


# ── 1. Create a dummy PDF in memory ─────────────────────────────────
def make_dummy_pdf() -> BytesIO:
    """Generate a 2-page HR policy PDF in memory."""
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=LETTER)
    styles = getSampleStyleSheet()

    story = [
        Paragraph("Acme Corp — Employee Onboarding Policy", styles["Title"]),
        Spacer(1, 0.3 * inch),
        Paragraph(
            "Section 1: New Hire Orientation. "
            "All new employees must complete a mandatory orientation session within "
            "their first five business days. The orientation covers company history, "
            "organizational structure, IT security policies, and benefits enrollment. "
            "Employees must sign the Code of Conduct and the Data Protection Agreement "
            "before receiving access to internal systems.",
            styles["BodyText"],
        ),
        Spacer(1, 0.2 * inch),
        Paragraph(
            "Section 2: Equipment & Access. "
            "The IT department will provision a company laptop, email account, and "
            "badge within 48 hours of the employee's start date. Managers must submit "
            "an access request via the HR portal at least three days before the start "
            "date. Remote employees receive equipment via overnight courier.",
            styles["BodyText"],
        ),
        Spacer(1, 0.2 * inch),
        Paragraph(
            "Section 3: Probation Period. "
            "All new hires are subject to a 90-day probationary period. During this "
            "time, the hiring manager must conduct bi-weekly check-ins and submit a "
            "formal 30-60-90 day review. If performance expectations are not met, the "
            "employment may be terminated with a two-week notice.",
            styles["BodyText"],
        ),
        Spacer(1, 0.2 * inch),
        Paragraph(
            "Section 4: Leave Policy. "
            "Employees are entitled to 15 days of paid time off (PTO) per year, "
            "accruing at 1.25 days per month. Sick leave is separate at 10 days per "
            "year. PTO requests must be submitted at least two weeks in advance for "
            "absences longer than three consecutive days.",
            styles["BodyText"],
        ),
    ]

    doc.build(story)
    buf.seek(0)
    buf.name = "acme_onboarding_policy.pdf"  # mimic Streamlit UploadedFile
    return buf


def main():
    logger.info("=" * 60)
    logger.info("RAG PIPELINE END-TO-END TEST")
    logger.info("=" * 60)

    # ── Step 1: Ingest ───────────────────────────────────────────────
    from rag.ingest import ingest_pdfs

    dummy_pdf = make_dummy_pdf()
    logger.info("Created dummy PDF: %s", dummy_pdf.name)

    chunks, warnings = ingest_pdfs([dummy_pdf])

    if warnings:
        for w in warnings:
            logger.warning("Ingest warning: %s", w)

    assert len(chunks) > 0, "Expected at least 1 chunk, got 0"
    logger.info("✅ Ingest OK — %d chunks created.", len(chunks))

    for i, c in enumerate(chunks[:3]):
        logger.info(
            "  Chunk %d: source=%s, page=%s, len=%d",
            i + 1,
            c.metadata.get("source"),
            c.metadata.get("page"),
            len(c.page_content),
        )

    # ── Step 2: Edge cases ───────────────────────────────────────────
    empty_chunks, empty_warnings = ingest_pdfs([])
    assert len(empty_chunks) == 0
    assert any("No PDF" in w for w in empty_warnings)
    logger.info("✅ Edge case OK — empty input returns warning.")

    # ── Step 3: Build vector store ───────────────────────────────────
    from rag.vectorstore import build_vectorstore, load_vectorstore, index_exists, clear_vectorstore

    # Clean up any previous test index
    clear_vectorstore()
    assert not index_exists(), "Index should not exist after clear."

    db = build_vectorstore(chunks)
    assert db is not None
    assert index_exists(), "Index should exist after build."
    logger.info("✅ Vectorstore build OK — index persisted.")

    # ── Step 4: Load vector store ────────────────────────────────────
    db2 = load_vectorstore()
    assert db2 is not None
    logger.info("✅ Vectorstore load OK — index reloaded from disk.")

    # ── Step 5: Retrieve ─────────────────────────────────────────────
    from rag.retrieval import retrieve, format_context

    results = retrieve("What is the probation period policy?", k=3)
    assert len(results) > 0, "Expected at least 1 retrieval result."
    logger.info("✅ Retrieval OK — %d results.", len(results))

    for i, r in enumerate(results):
        logger.info(
            "  Result %d: source=%s, page=%d, score=%.4f, text=%.80s…",
            i + 1, r["source"], r["page"], r["score"], r["text"],
        )

    # Format context
    ctx = format_context(results)
    assert "[Source 1:" in ctx
    logger.info("✅ format_context OK — %d chars.", len(ctx))

    # ── Step 6: Clean up ─────────────────────────────────────────────
    clear_vectorstore()
    logger.info("✅ Cleanup OK — index files removed.")

    logger.info("=" * 60)
    logger.info("ALL TESTS PASSED")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
