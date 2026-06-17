from __future__ import annotations

import logging
from typing import Any, Dict

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors

from utils.gemini_client import get_chat_llm
from utils.helpers import call_gemini_json
from prompts.generator_prompt import (
    GENERATOR_SYSTEM_PROMPT,
    build_generator_user_prompt,
)

logger = logging.getLogger(__name__)


def generate_documents(
    reasoning_output: Dict[str, Any],
    compliance_output: Dict[str, Any],
    employee_name: str,
    role: str,
) -> Dict[str, Any]:
    """Draft exactly 4 dynamic markdown documents based on the workflow.

    Returns
    -------
    dict
        Parsed JSON containing 4 dynamic titles and markdown bodies.
    """
    logger.info("Generating documents for '%s' (%s) …", employee_name, role)

    llm = get_chat_llm(temperature=0.3)
    user_prompt = build_generator_user_prompt(
        reasoning_output=reasoning_output,
        compliance_output=compliance_output,
        employee_name=employee_name,
        role=role,
    )

    fallback = {
        "doc_1_title": "Document 1",
        "doc_1_md": "Error generating document.",
        "doc_2_title": "Document 2",
        "doc_2_md": "Error generating document.",
        "doc_3_title": "Document 3",
        "doc_3_md": "Error generating document.",
        "doc_4_title": "Document 4",
        "doc_4_md": "Error generating document.",
    }

    result = call_gemini_json(
        llm=llm,
        system_prompt=GENERATOR_SYSTEM_PROMPT,
        user_content=user_prompt,
        fallback=fallback,
    )
    
    # Ensure all required keys exist to prevent downstream KeyErrors
    for i in range(1, 5):
        if f"doc_{i}_title" not in result:
            result[f"doc_{i}_title"] = fallback[f"doc_{i}_title"]
        if f"doc_{i}_md" not in result:
            result[f"doc_{i}_md"] = fallback[f"doc_{i}_md"]

    return result


def export_to_pdf(generated_docs: Dict[str, Any], filename: str = "workflow_output.pdf") -> str:
    """Export the 4 dynamic markdown documents into a polished PDF.

    Currently uses a basic parser to convert simple Markdown (## and - )
    into ReportLab Paragraphs.

    Parameters
    ----------
    generated_docs : dict
        Output from ``generate_documents()``.
    filename : str
        Desired output filename (e.g. "offboarding_ahmed.pdf").

    Returns
    -------
    str
        The path to the generated PDF.
    """
    import os
    import re

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()
    
    # Customise styles
    title_style = ParagraphStyle(
        "WorkflowTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=colors.teal,
        spaceAfter=20,
    )
    h1_style = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.darkblue,
        spaceAfter=12,
    )
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.darkslategray,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=10,
        leading=16,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        fontSize=11,
        leftIndent=20,
        spaceAfter=6,
        leading=16,
    )

    story = []

    # Title Page
    story.append(Paragraph("PolicyPilot AI", title_style))
    story.append(Paragraph("Generated Workflow Documentation", h1_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("This document contains all auto-generated artifacts for the requested workflow.", body_style))
    story.append(PageBreak())

    def _md_to_story(md_text: str):
        lines = md_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Convert bold (**text**) to ReportLab bold (<b>text</b>)
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)

            if line.startswith('### '):
                story.append(Paragraph(line[4:], h2_style))
            elif line.startswith('## '):
                story.append(Paragraph(line[3:], h1_style))
            elif line.startswith('# '):
                story.append(Paragraph(line[2:], title_style))
            elif line.startswith('- ') or line.startswith('* '):
                story.append(Paragraph(u"• " + line[2:], bullet_style))
            elif re.match(r'^\d+\.\s', line):
                story.append(Paragraph(line, bullet_style))
            else:
                story.append(Paragraph(line, body_style))
        story.append(Spacer(1, 20))

    # Loop through the 4 dynamic documents
    for i in range(1, 5):
        title = generated_docs.get(f"doc_{i}_title", f"Document {i}")
        md_content = generated_docs.get(f"doc_{i}_md", "")
        
        story.append(Paragraph(title, h1_style))
        _md_to_story(md_content)
        if i < 4:
            story.append(PageBreak())

    try:
        doc.build(story)
        logger.info("PDF exported successfully to %s", pdf_path)
    except Exception as e:
        logger.error("Failed to build PDF: %s", e)

    return pdf_path
