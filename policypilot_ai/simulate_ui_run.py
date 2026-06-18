"""
End-to-end UI Simulation Test.

Ingests the 3 sample PDFs, runs the pipeline for "Onboard Ahmed as a Software Engineer",
and validates the outputs explicitly check for things mentioned in the PDFs (like NDA).
"""

import sys
import json
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline import run_pipeline
from rag.ingest import ingest_pdfs
from rag.vectorstore import build_vectorstore, clear_vectorstore
from config import SAMPLE_DOCS_DIR

logging.basicConfig(level=logging.INFO, format="%(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger("ui_simulator")

def main():
    logger.info("=" * 60)
    logger.info("STARTING END-TO-END UI SIMULATION")
    logger.info("=" * 60)

    # 1. Ingest the generated PDFs
    pdf_files = list(SAMPLE_DOCS_DIR.glob("*.pdf"))
    if not pdf_files:
        logger.error("No PDFs found in sample_docs/. Did you run generate_samples.py?")
        sys.exit(1)

    logger.info("Ingesting %d PDFs...", len(pdf_files))
    chunks, warnings = ingest_pdfs(pdf_files)
    if warnings:
        for w in warnings:
            logger.warning(w)

    clear_vectorstore()
    build_vectorstore(chunks)
    logger.info("Vectorstore built with %d chunks.", len(chunks))

    # 2. Run the pipeline
    user_task = "Onboard Ahmed as a Software Engineer"
    employee_name = "Ahmed"
    role = "Software Engineer"
    
    logger.info("Running pipeline...")
    result = run_pipeline(user_task, employee_name, role)

    # 3. Validation
    assert result["status"] == "success", f"Pipeline failed: {result.get('error_message')}"
    
    reasoning = result["reasoning"]
    compliance = result["compliance"]
    generation = result["generation"]

    logger.info("Pipeline completed successfully.")
    
    # Check if NDA is caught
    docs_required = reasoning.get("required_documents", [])
    has_nda = any("NDA" in d.upper() or "NON-DISCLOSURE" in d.upper() for d in docs_required)
    if has_nda:
        logger.info("✅ Reasoning agent correctly identified NDA requirement.")
    else:
        logger.error("❌ Reasoning agent missed the NDA requirement. Docs found: %s", docs_required)
        
    # Check if MacBook requirement is caught
    actions = reasoning.get("actions", [])
    has_macbook = any("MACBOOK" in a.upper() or "LAPTOP" in a.upper() or "PROVISION" in a.upper() for a in actions)
    if has_macbook:
        logger.info("✅ Reasoning agent correctly identified equipment provisioning.")
    else:
        logger.error("❌ Reasoning agent missed the equipment requirement. Actions found: %s", actions)

    # Check checklist
    checklist = generation.get("checklist_md", "")
    if "NDA" in checklist.upper():
         logger.info("✅ Checklist correctly includes NDA.")
    else:
         logger.error("❌ Checklist missing NDA.")
         
    # Validate PDF
    pdf_path = result.get("pdf_path")
    if pdf_path and Path(pdf_path).exists():
        logger.info("✅ Generated PDF exists at %s", pdf_path)
    else:
        logger.error("❌ PDF not generated properly.")
        
    logger.info("=" * 60)
    logger.info("SIMULATION FINISHED.")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
