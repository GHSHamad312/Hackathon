"""
End-to-end test for the main orchestration pipeline.
"""

import sys
import logging
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline import run_pipeline

logging.basicConfig(level=logging.INFO, format="%(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger("test_pipeline")


def main():
    # ── Setup: build FAISS index from test docs ──────────────────────
    from test_agents import make_dummy_pdf
    from rag.ingest import ingest_pdfs
    from rag.vectorstore import build_vectorstore, clear_vectorstore

    logger.info("Setting up test vectorstore...")
    dummy_pdf = make_dummy_pdf()
    chunks, _ = ingest_pdfs([dummy_pdf])
    clear_vectorstore()
    build_vectorstore(chunks)

    # ── Run Pipeline ─────────────────────────────────────────────────
    user_task = "Onboard Ali as a Data Analyst"
    employee_name = "Ali"
    role = "Data Analyst"

    logger.info("Running pipeline with task: '%s'", user_task)
    result = run_pipeline(user_task, employee_name, role)

    # ── Verify Results ───────────────────────────────────────────────
    assert isinstance(result, dict), "Pipeline should return a dict."
    
    expected_keys = [
        "planner", "retrieval", "reasoning", "compliance",
        "generation", "action", "pdf_path", "status", "failed_stage"
    ]
    for key in expected_keys:
        assert key in result, f"Missing key in pipeline result: {key}"

    assert result["status"] == "success", f"Pipeline failed at stage: {result['failed_stage']}. Error: {result.get('error_message')}"
    
    # Check that each stage has data
    assert result["planner"].get("tasks"), "Planner tasks empty"
    assert len(result["retrieval"]) > 0, "Retrieval empty"
    assert result["reasoning"].get("summary"), "Reasoning summary empty"
    assert "compliance_score" in result["compliance"], "Compliance score missing"
    assert result["generation"].get("checklist_md"), "Generation checklist missing"
    assert result["action"].get("hr_ticket"), "Action status missing"
    assert result["pdf_path"] and Path(result["pdf_path"]).exists(), "PDF not generated or path invalid"

    logger.info("\nPipeline Result Summary:")
    logger.info("Status: %s", result["status"])
    logger.info("Planner tasks: %d", len(result["planner"]["tasks"]))
    logger.info("Retrieved passages: %d", len(result["retrieval"]))
    logger.info("Compliance score: %s", result["compliance"]["compliance_score"])
    logger.info("Generated PDF: %s", result["pdf_path"])
    
    logger.info("\n============================================================")
    logger.info("PIPELINE TEST PASSED")
    logger.info("============================================================")

    # Clean up
    clear_vectorstore()
    pdf_file = Path(result["pdf_path"])
    if pdf_file.exists():
        pdf_file.unlink()

if __name__ == "__main__":
    main()
