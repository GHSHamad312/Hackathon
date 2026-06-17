"""
End-to-end test for all six PolicyPilot AI agents.

Creates a dummy PDF, builds a FAISS index, then runs the full pipeline:
  Planner → Retriever → Reasoning → Compliance → Generator → Action

Each agent is validated for correct output shape and no exceptions.
"""

import sys
import json
import logging
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

logging.basicConfig(level=logging.INFO, format="%(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger("test_agents")

PASS = "✅"
FAIL = "❌"


# ── Helpers ──────────────────────────────────────────────────────────

def make_dummy_pdf() -> BytesIO:
    """Generate a multi-section HR policy PDF in memory."""
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Acme Corp — Employee Onboarding Policy", styles["Title"]),
        Spacer(1, 0.3 * inch),
        Paragraph(
            "Section 1: New Hire Orientation. All new employees must complete "
            "a mandatory orientation session within their first five business "
            "days. The orientation covers company history, organizational "
            "structure, IT security policies, and benefits enrollment. "
            "Employees must sign the Code of Conduct and the Data Protection "
            "Agreement before receiving access to internal systems.",
            styles["BodyText"],
        ),
        Spacer(1, 0.2 * inch),
        Paragraph(
            "Section 2: Equipment & Access. The IT department will provision "
            "a company laptop, email account, and badge within 48 hours of "
            "the employee's start date. Managers must submit an access request "
            "via the HR portal at least three days before the start date. "
            "Remote employees receive equipment via overnight courier.",
            styles["BodyText"],
        ),
        Spacer(1, 0.2 * inch),
        Paragraph(
            "Section 3: Probation Period. All new hires are subject to a "
            "90-day probationary period. During this time, the hiring manager "
            "must conduct bi-weekly check-ins and submit a formal 30-60-90 "
            "day review. If performance expectations are not met, employment "
            "may be terminated with a two-week notice.",
            styles["BodyText"],
        ),
        Spacer(1, 0.2 * inch),
        Paragraph(
            "Section 4: Required Documents. New employees must provide: "
            "government-issued photo ID, proof of address, signed offer "
            "letter, completed tax forms (W-4), emergency contact information, "
            "and bank account details for direct deposit. International "
            "employees must additionally provide work authorization documents.",
            styles["BodyText"],
        ),
    ]
    doc.build(story)
    buf.seek(0)
    buf.name = "acme_onboarding_policy.pdf"
    return buf


def assert_keys(result: dict, required_keys: list, label: str):
    """Assert that *result* contains all *required_keys*."""
    missing = [k for k in required_keys if k not in result]
    if missing:
        raise AssertionError(f"{label}: missing keys {missing} in {list(result.keys())}")


# ── Main test ────────────────────────────────────────────────────────

def main():
    logger.info("=" * 60)
    logger.info("AGENT PIPELINE END-TO-END TEST")
    logger.info("=" * 60)

    # ── Setup: build FAISS index from dummy PDF ──────────────────────
    from rag.ingest import ingest_pdfs
    from rag.vectorstore import build_vectorstore, clear_vectorstore

    dummy_pdf = make_dummy_pdf()
    chunks, warnings = ingest_pdfs([dummy_pdf])
    assert len(chunks) > 0, "Ingest produced no chunks."
    logger.info("Setup: ingested %d chunks.", len(chunks))

    clear_vectorstore()
    build_vectorstore(chunks)
    logger.info("Setup: FAISS index built.\n")

    # ── 1. Planner ───────────────────────────────────────────────────
    from agents.planner import plan

    plan_result = plan("Onboard Ahmed as a Software Engineer")
    assert isinstance(plan_result, dict), "Planner should return dict."
    assert_keys(plan_result, ["goal", "tasks"], "Planner")
    assert len(plan_result["tasks"]) > 0, "Planner should produce tasks."
    logger.info("%s Planner OK — %d tasks.", PASS, len(plan_result["tasks"]))
    logger.info("   Goal: %s", plan_result["goal"])
    for i, t in enumerate(plan_result["tasks"], 1):
        logger.info("   %d. %s", i, t)

    # ── 2. Retriever ─────────────────────────────────────────────────
    from agents.retriever import retrieve_for_tasks

    passages = retrieve_for_tasks(plan_result["tasks"])
    assert isinstance(passages, list), "Retriever should return list."
    assert len(passages) > 0, "Retriever should find passages."
    logger.info("%s Retriever OK — %d unique passages.", PASS, len(passages))

    # ── 3. Reasoning ─────────────────────────────────────────────────
    from agents.reasoning import reason

    reasoning_result = reason(
        user_task="Onboard Ahmed as a Software Engineer",
        retrieved_passages=passages,
        plan=plan_result,
    )
    assert isinstance(reasoning_result, dict), "Reasoning should return dict."
    assert_keys(
        reasoning_result,
        ["summary", "required_documents", "actions", "departments", "dependencies"],
        "Reasoning",
    )
    logger.info("%s Reasoning OK — summary: %.80s…", PASS, reasoning_result["summary"])

    # ── 4. Compliance ────────────────────────────────────────────────
    from agents.compliance import check_compliance

    compliance_result = check_compliance(
        reasoning_output=reasoning_result,
        retrieved_passages=passages,
    )
    assert isinstance(compliance_result, dict), "Compliance should return dict."
    assert_keys(
        compliance_result,
        ["compliance_score", "missing_requirements", "warnings", "recommendations"],
        "Compliance",
    )
    logger.info(
        "%s Compliance OK — score: %s, %d warning(s).",
        PASS,
        compliance_result["compliance_score"],
        len(compliance_result["warnings"]),
    )

    # ── 5. Generator ─────────────────────────────────────────────────
    from agents.generator import generate_documents, export_to_pdf

    gen_result = generate_documents(
        reasoning_output=reasoning_result,
        compliance_output=compliance_result,
        employee_name="Ahmed",
        role="Software Engineer",
    )
    assert isinstance(gen_result, dict), "Generator should return dict."
    assert_keys(
        gen_result,
        ["checklist_md", "welcome_email_md", "hr_summary_md", "manager_summary_md"],
        "Generator",
    )
    logger.info("%s Generator OK — 4 document sections produced.", PASS)

    # Test PDF export
    pdf_path = export_to_pdf(gen_result, filename="test_onboarding.pdf")
    assert Path(pdf_path).exists(), f"PDF should exist at {pdf_path}."
    logger.info("%s PDF export OK — %s", PASS, pdf_path)

    # ── 6. Action ────────────────────────────────────────────────────
    from agents.action import simulate_actions

    action_result = simulate_actions(gen_result)
    assert isinstance(action_result, dict), "Action should return dict."
    assert_keys(
        action_result,
        ["hr_ticket", "it_ticket", "welcome_email", "employee_id_request", "pdf_download"],
        "Action",
    )
    logger.info("%s Action OK — statuses: %s", PASS, json.dumps(action_result, indent=2))

    # ── Cleanup ──────────────────────────────────────────────────────
    clear_vectorstore()
    # Clean up test PDF
    test_pdf = Path(pdf_path)
    if test_pdf.exists():
        test_pdf.unlink()
        logger.info("Cleaned up test PDF.")

    logger.info("\n" + "=" * 60)
    logger.info("ALL 6 AGENTS PASSED")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
