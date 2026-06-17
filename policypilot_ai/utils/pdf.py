"""
PDF utilities — extraction (pypdf) and generation (reportlab).
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import List

from pypdf import PdfReader
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from config import OUTPUTS_DIR


# ── Extraction ───────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Read all pages of a PDF and return the concatenated text."""
    reader = PdfReader(str(pdf_path))
    pages: List[str] = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages)


# ── Generation ───────────────────────────────────────────────────────

def generate_pdf_report(
    title: str,
    body: str,
    filename: str = "report.pdf",
) -> Path:
    """Create a simple PDF report and return its path inside outputs/."""
    out_path = OUTPUTS_DIR / filename
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=LETTER,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=14,
    )
    body_style = styles["BodyText"]

    story = [
        Paragraph(title, title_style),
        Spacer(1, 0.25 * inch),
    ]

    for para in body.split("\n\n"):
        cleaned = para.strip().replace("\n", "<br/>")
        if cleaned:
            story.append(Paragraph(cleaned, body_style))
            story.append(Spacer(1, 0.15 * inch))

    doc.build(story)
    return out_path
