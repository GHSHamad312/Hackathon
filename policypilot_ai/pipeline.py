"""
Main orchestration pipeline for PolicyPilot AI.

Executes the multi-agent pipeline in sequence:
Planner → Retriever → Reasoning → Compliance → Generator → Action.

Includes comprehensive error boundaries. If any stage fails, the pipeline
halts gracefully and returns the partial results gathered up to that point.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict

from agents.planner import plan
from agents.retriever import retrieve_for_tasks
from agents.reasoning import reason
from agents.compliance import check_compliance
from agents.generator import generate_documents, export_to_pdf
from agents.action import simulate_actions

logger = logging.getLogger(__name__)


def run_pipeline(
    user_task: str,
    employee_name: str,
    role: str,
) -> Dict[str, Any]:
    """Execute the full agentic pipeline.

    Parameters
    ----------
    user_task : str
        The high-level user request (e.g., "Onboard Ali as a Data Analyst").
    employee_name : str
        The employee's name for document generation.
    role : str
        The employee's role for document generation.

    Returns
    -------
    dict
        A complete state object containing outputs from every stage:
        {
            "planner": dict,
            "retrieval": list,
            "reasoning": dict,
            "compliance": dict,
            "generation": dict,
            "action": dict,
            "pdf_path": str | None,
            "status": "success" | "partial_failure",
            "failed_stage": str | None,
            "error_message": str | None
        }
    """
    logger.info("=" * 60)
    logger.info("PIPELINE START: %s", user_task)
    logger.info("=" * 60)

    # Output state container
    state: Dict[str, Any] = {
        "planner": {},
        "retrieval": [],
        "reasoning": {},
        "compliance": {},
        "generation": {},
        "action": {},
        "pdf_path": None,
        "status": "success",
        "failed_stage": None,
        "error_message": None,
    }

    # ── Stage 1: Planner ─────────────────────────────────────────────
    stage = "planner"
    _log_stage_start(stage)
    start_time = time.time()
    try:
        planner_result = plan(user_task)
        if "error" in planner_result:
            raise RuntimeError(planner_result["error"])
        state["planner"] = planner_result
        _log_stage_end(stage, start_time)
    except Exception as exc:
        return _handle_failure(state, stage, exc)

    # ── Stage 2: Retrieval ───────────────────────────────────────────
    stage = "retrieval"
    _log_stage_start(stage)
    start_time = time.time()
    try:
        tasks = state["planner"].get("tasks", [])
        retrieval_result = retrieve_for_tasks(tasks)
        # We don't fail if retrieval is empty (maybe there are no PDFs yet),
        # we just proceed with an empty context.
        state["retrieval"] = retrieval_result
        _log_stage_end(stage, start_time)
    except Exception as exc:
        return _handle_failure(state, stage, exc)

    # ── Stage 3: Reasoning ───────────────────────────────────────────
    stage = "reasoning"
    _log_stage_start(stage)
    start_time = time.time()
    try:
        reasoning_result = reason(
            user_task=user_task,
            retrieved_passages=state["retrieval"],
            plan=state["planner"],
        )
        if "error" in reasoning_result:
            raise RuntimeError(reasoning_result["error"])
        state["reasoning"] = reasoning_result
        _log_stage_end(stage, start_time)
    except Exception as exc:
        return _handle_failure(state, stage, exc)

    # ── Stage 4: Compliance ──────────────────────────────────────────
    stage = "compliance"
    _log_stage_start(stage)
    start_time = time.time()
    try:
        compliance_result = check_compliance(
            reasoning_output=state["reasoning"],
            retrieved_passages=state["retrieval"],
        )
        if "error" in compliance_result:
            raise RuntimeError(compliance_result["error"])
        state["compliance"] = compliance_result
        _log_stage_end(stage, start_time)
    except Exception as exc:
        return _handle_failure(state, stage, exc)

    # ── Stage 5: Generation & PDF Export ─────────────────────────────
    stage = "generation"
    _log_stage_start(stage)
    start_time = time.time()
    try:
        gen_result = generate_documents(
            reasoning_output=state["reasoning"],
            compliance_output=state["compliance"],
            employee_name=employee_name,
            role=role,
        )
        if "error" in gen_result:
            raise RuntimeError(gen_result["error"])
        state["generation"] = gen_result

        # Export PDF
        pdf_filename = f"onboarding_{employee_name.replace(' ', '_').lower()}.pdf"
        pdf_path = export_to_pdf(gen_result, filename=pdf_filename)
        state["pdf_path"] = pdf_path
        _log_stage_end(stage, start_time)
    except Exception as exc:
        return _handle_failure(state, stage, exc)

    # ── Stage 6: Action ──────────────────────────────────────────────
    stage = "action"
    _log_stage_start(stage)
    start_time = time.time()
    try:
        action_result = simulate_actions(state["generation"])
        if "error" in action_result:
            raise RuntimeError(action_result["error"])
        state["action"] = action_result
        _log_stage_end(stage, start_time)
    except Exception as exc:
        return _handle_failure(state, stage, exc)

    logger.info("PIPELINE SUCCESS!")
    return state


# ── Internal Helpers ─────────────────────────────────────────────────

def _log_stage_start(stage: str):
    """Log the beginning of a pipeline stage."""
    logger.info(">>> STARTING STAGE: [%s]", stage.upper())


def _log_stage_end(stage: str, start_time: float):
    """Log the successful completion of a pipeline stage."""
    elapsed = time.time() - start_time
    logger.info("<<< COMPLETED STAGE: [%s] in %.2f seconds.", stage.upper(), elapsed)


def _handle_failure(state: Dict[str, Any], stage: str, exc: Exception) -> Dict[str, Any]:
    """Update state on failure, log the error, and return the partial state."""
    logger.error("!!! PIPELINE FAILED AT STAGE: [%s]", stage.upper(), exc_info=True)
    state["status"] = "partial_failure"
    state["failed_stage"] = stage
    state["error_message"] = str(exc)
    return state
