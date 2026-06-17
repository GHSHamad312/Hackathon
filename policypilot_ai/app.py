"""
PolicyPilot AI — Streamlit Frontend (v3 — Enterprise Polish).

A polished enterprise SaaS interface combining a multi-agent workflow
with RAG capabilities, policy Q&A chat, agent tracing, workflow history,
and a metrics dashboard.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

import streamlit as st

# ── Page Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="PolicyPilot AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ── Animated gradient header ── */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #0d9488 50%, #0f172a 100%);
        padding: 3rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
        animation: shimmer 12s linear infinite;
    }
    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        position: relative;
        z-index: 1;
        letter-spacing: -0.02em;
    }
    .hero-tagline {
        font-size: 1.25rem;
        color: #cbd5e1;
        font-weight: 400;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        color: #f8fafc;
        padding: 0.35rem 1rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 1.2rem;
        position: relative;
        z-index: 1;
        backdrop-filter: blur(8px);
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ── Metric cards ── */
    .metric-row {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        flex: 1;
        background: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }

    /* ── Shadow cards ── */
    .card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1rem;
    }
    .doc-preview {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #0d9488;
        font-size: 0.95rem;
        max-height: 600px;
        overflow-y: auto;
        color: #334155;
        line-height: 1.6;
    }

    /* ── Badges ── */
    .badge-excellent { background: #dcfce7; color: #166534; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; }
    .badge-warning  { background: #fef3c7; color: #92400e; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; }
    .badge-danger   { background: #fee2e2; color: #991b1b; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; }

    /* ── Warning box ── */
    .warning-box {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 5px solid #f59e0b;
        padding: 1.25rem;
        border-radius: 8px;
        color: #92400e;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .warning-box strong {
        display: block;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: #b45309;
    }
    .warning-box ul {
        margin-top: 0.5rem;
        margin-bottom: 0;
        padding-left: 1.5rem;
    }
    .warning-box li {
        margin-bottom: 0.25rem;
    }

    /* ── Chat messages ── */
    .chat-user {
        background: #f0fdfa;
        border-radius: 12px 12px 4px 12px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        border: 1px solid #ccfbf1;
        color: #0f766e;
    }
    .chat-ai {
        background: #ffffff;
        border-radius: 12px 12px 12px 4px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        color: #334155;
    }

    /* ── Timeline ── */
    .timeline-item {
        border-left: 3px solid #0d9488;
        padding: 1rem 1.25rem;
        margin-left: 1rem;
        margin-bottom: 0.75rem;
        background: #f8fafc;
        border-radius: 0 8px 8px 0;
        border: 1px solid #f1f5f9;
        border-left: none;
        transition: background 0.2s ease;
    }
    .timeline-item:hover {
        background: #f1f5f9;
    }
    .timeline-header {
        font-weight: 700;
        color: #0f172a;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }
    .timeline-meta {
        font-size: 0.85rem;
        color: #64748b;
    }

    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #64748b;
        transition: color 0.2s ease;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #0d9488;
    }
    
    /* ── Action Items ── */
    .action-item {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .action-icon {
        font-size: 1.25rem;
    }
    .action-label {
        font-weight: 600;
        color: #1e293b;
        flex: 1;
    }
    .action-status {
        background: #f1f5f9;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        color: #475569;
        font-family: monospace;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Imports ───────────────────────────────────────────────────────────
from config import api_key_is_set, GOOGLE_API_KEY
from rag.ingest import ingest_pdfs
from rag.vectorstore import build_vectorstore, index_exists
from rag.retrieval import retrieve, format_context
from agents.planner import plan
from agents.retriever import retrieve_for_tasks
from agents.reasoning import reason
from agents.compliance import check_compliance
from agents.generator import generate_documents, export_to_pdf
from agents.action import simulate_actions

# ── Session State Init ───────────────────────────────────────────────
defaults = {
    "temp_api_key": "",
    "pipeline_result": None,
    "agent_trace": {},
    "workflow_history": [],
    "chat_messages": [],
    "chunks_indexed": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈️ PolicyPilot AI")
    st.caption("Enterprise Workflow Automation Engine")
    
    st.markdown("---")
    
    # Simple status indicator for API key in sidebar
    has_env_key = api_key_is_set()
    has_temp_key = bool(st.session_state["temp_api_key"].strip())
    is_authenticated = has_env_key or has_temp_key
    
    if is_authenticated:
        st.success("🔒 System Authenticated")
    else:
        st.error("🔓 Authentication Required")

    st.markdown("---")
    st.markdown("##### 📚 Knowledge Base Setup")
    st.info("Upload your company policies (HR, IT, SOPs) to create the AI's source of truth.", icon="ℹ️")
    
    uploaded_files = st.file_uploader(
        "Upload Policy Documents (PDF)",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if st.button("Build Knowledge Base", use_container_width=True, type="primary"):
        if not uploaded_files:
            st.warning("Please upload at least one PDF first.")
        else:
            with st.spinner("Processing and indexing documents..."):
                chunks, warnings = ingest_pdfs(uploaded_files)
                if warnings:
                    for w in warnings:
                        st.sidebar.warning(w)
                if chunks:
                    build_vectorstore(chunks)
                    st.session_state["chunks_indexed"] = len(chunks)
                    st.success(f"✅ Successfully indexed {len(chunks)} text chunks from {len(uploaded_files)} document(s)!")
                else:
                    st.error("Failed to extract text from the provided PDFs.")

    if index_exists():
        st.caption("🟢 Vector store is active and ready.")
    else:
        st.caption("🔴 Vector store is empty.")

    st.markdown("---")
    st.markdown("##### 📊 Session Overview")
    col_s1, col_s2 = st.columns(2)
    col_s1.metric("Workflows Run", len(st.session_state["workflow_history"]))
    col_s2.metric("Knowledge Chunks", st.session_state["chunks_indexed"])


# ══════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════

# ── Hero Header ──────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">PolicyPilot AI</div>
        <div class="hero-tagline">The autonomous compliance & workflow engine for modern enterprises.</div>
        <span class="hero-badge">⚡ Agentic AI Architecture</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Onboarding / Authentication Screen ───────────────────────────────
if not is_authenticated:
    st.markdown("### Welcome to PolicyPilot AI")
    st.markdown("""
    PolicyPilot AI uses a **6-Agent Architecture** to fully automate HR and IT workflows while guaranteeing 100% compliance with your company's actual policies.
    
    To get started, you need to connect the engine to the Google Gemini API.
    """)
    
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### 🔑 Connect Your Enterprise API Key")
        st.markdown("Enter your Gemini API key below. Your key is stored securely in memory and will be cleared when your session ends.")
        
        api_key_input = st.text_input(
            "Google Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            help="Get your API key from Google AI Studio."
        )
        
        if st.button("Authenticate System", type="primary"):
            if api_key_input.strip():
                st.session_state["temp_api_key"] = api_key_input.strip()
                os.environ["GOOGLE_API_KEY"] = api_key_input.strip()
                st.rerun()
            else:
                st.error("Please enter a valid API key.")
    
    with col2:
        st.info(
            "**System Architecture:**\n\n"
            "1. **Planner Agent**\n"
            "2. **Retrieval Agent**\n"
            "3. **Reasoning Agent**\n"
            "4. **Compliance Agent**\n"
            "5. **Generator Agent**\n"
            "6. **Action Agent**\n"
        )
    st.stop()


# ── Main Application ─────────────────────────────────────────────────
# Tabs definition
tab_workflow, tab_chat, tab_history, tab_trace = st.tabs(
    ["🚀 Launch Workflow", "💬 Policy Q&A", "📜 Execution History", "🔍 Architecture Trace"]
)

# ══════════════════════════════════════════════════════════════════════
# TAB 1: WORKFLOW
# ══════════════════════════════════════════════════════════════════════
with tab_workflow:
    
    st.markdown("### System Configuration")
    
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            workflow_type = st.selectbox(
                "Select Enterprise Workflow",
                [
                    "Employee Onboarding",
                    "Employee Offboarding",
                    "Internal Role Transfer",
                    "Leave of Absence Processing",
                    "Performance Improvement Plan (PIP)",
                    "Policy Compliance Audit",
                    "Custom Task..."
                ],
                help="Select the standardized procedure, or choose Custom Task for free-form requests."
            )
            
            emp_name = st.text_input("Target Subject Name", placeholder="e.g., Sarah Chen")
            emp_role = st.text_input("Subject Context / Title", placeholder="e.g., Senior Data Scientist")
            
        with col2:
            default_task = f"Execute {workflow_type} procedures for {emp_name} ({emp_role}). Ensure all compliance protocols are followed." if emp_name else ""
            if workflow_type == "Custom Task...":
                default_task = ""
                
            user_task = st.text_area(
                "Specific Workflow Directives", 
                placeholder="Enter exact instructions, exceptions, or specific requirements here...",
                value=default_task,
                height=180,
                help="The AI will interpret these instructions and audit them against company policy."
            )
            
        submitted = st.button("🚀 Initialize Multi-Agent Pipeline", type="primary", use_container_width=True)

    # ── Execute Pipeline ─────────────────────────────────────────────
    if submitted:
        if not user_task or not emp_name or not emp_role:
            st.warning("Please fill in all subject details and directives before launching the pipeline.")
            st.stop()
        if not index_exists():
            st.warning(
                "⚠️ Knowledge Base Warning: No vector store found. The AI will operate without policy context. Please upload policies in the sidebar for optimal results."
            )

        state = {}
        trace = {}
        pipeline_start = time.time()
        st.markdown("---")
        st.markdown("### ⚙️ Pipeline Execution")

        # 1. Planner
        try:
            with st.status("🗓️ **Agent 1: Task Planner** — Decomposing directives...", expanded=True) as s:
                t0 = time.time()
                planner_result = plan(user_task)
                elapsed = time.time() - t0
                if "error" in planner_result:
                    raise RuntimeError(planner_result["error"])
                state["planner"] = planner_result
                trace["planner"] = {"output": planner_result, "time_s": round(elapsed, 2)}
                task_count = len(planner_result.get("tasks", []))
                s.update(label=f"🗓️ **Agent 1: Task Planner** — ✔ Created {task_count} sub-tasks ({elapsed:.1f}s)", state="complete", expanded=False)
        except Exception as e:
            s.update(label="🗓️ **Agent 1: Task Planner** — ❌ Fatal Error", state="error")
            st.error(f"Planner failed: {e}")
            st.stop()

        # 2. Retrieval
        try:
            with st.status("🔍 **Agent 2: Policy Retriever** — Querying vector database...", expanded=True) as s:
                t0 = time.time()
                tasks = state["planner"].get("tasks", [])
                retrieval_result = retrieve_for_tasks(tasks)
                elapsed = time.time() - t0
                state["retrieval"] = retrieval_result
                trace["retrieval"] = {"passages_found": len(retrieval_result), "time_s": round(elapsed, 2)}
                s.update(label=f"🔍 **Agent 2: Policy Retriever** — ✔ Extracted {len(retrieval_result)} policy excerpts ({elapsed:.1f}s)", state="complete", expanded=False)
        except Exception as e:
            s.update(label="🔍 **Agent 2: Policy Retriever** — ❌ Fatal Error", state="error")
            st.error(f"Retrieval failed: {e}")
            st.stop()

        # 3. Reasoning
        try:
            with st.status("🧠 **Agent 3: Reasoner** — Synthesizing action plan...", expanded=True) as s:
                t0 = time.time()
                reasoning_result = reason(
                    user_task=user_task,
                    retrieved_passages=state["retrieval"],
                    plan=state["planner"],
                )
                elapsed = time.time() - t0
                if "error" in reasoning_result:
                    raise RuntimeError(reasoning_result["error"])
                state["reasoning"] = reasoning_result
                trace["reasoning"] = {"output": reasoning_result, "time_s": round(elapsed, 2)}
                action_count = len(reasoning_result.get("actions", []))
                s.update(label=f"🧠 **Agent 3: Reasoner** — ✔ Formulated {action_count} strategic actions ({elapsed:.1f}s)", state="complete", expanded=False)
        except Exception as e:
            s.update(label="🧠 **Agent 3: Reasoner** — ❌ Fatal Error", state="error")
            st.error(f"Reasoning failed: {e}")
            st.stop()

        # 4. Compliance
        try:
            with st.status("✅ **Agent 4: Compliance Auditor** — Auditing against corporate policy...", expanded=True) as s:
                t0 = time.time()
                compliance_result = check_compliance(
                    reasoning_output=state["reasoning"],
                    retrieved_passages=state["retrieval"],
                )
                elapsed = time.time() - t0
                if "error" in compliance_result:
                    raise RuntimeError(compliance_result["error"])
                state["compliance"] = compliance_result
                trace["compliance"] = {"output": compliance_result, "time_s": round(elapsed, 2)}
                score = compliance_result.get("compliance_score", 0)
                s.update(label=f"✅ **Agent 4: Compliance Auditor** — ✔ Audit Complete. Score: {score}/100 ({elapsed:.1f}s)", state="complete", expanded=False)
        except Exception as e:
            s.update(label="✅ **Agent 4: Compliance Auditor** — ❌ Fatal Error", state="error")
            st.error(f"Compliance failed: {e}")
            st.stop()

        # 5. Generator
        try:
            with st.status("📝 **Agent 5: Document Generator** — Drafting artifacts & applying self-correction...", expanded=True) as s:
                t0 = time.time()
                gen_result = generate_documents(
                    reasoning_output=state["reasoning"],
                    compliance_output=state["compliance"],
                    employee_name=emp_name,
                    role=emp_role,
                )
                elapsed = time.time() - t0
                if "error" in gen_result:
                    raise RuntimeError(gen_result["error"])
                state["generation"] = gen_result
                pdf_filename = f"{workflow_type.split()[0].lower()}_{emp_name.replace(' ', '_').lower()}.pdf"
                pdf_path = export_to_pdf(gen_result, filename=pdf_filename)
                state["pdf_path"] = pdf_path
                trace["generator"] = {"sections": list(gen_result.keys()), "time_s": round(elapsed, 2)}
                s.update(label=f"📝 **Agent 5: Document Generator** — ✔ Compiled compliant document packet ({elapsed:.1f}s)", state="complete", expanded=False)
        except Exception as e:
            s.update(label="📝 **Agent 5: Document Generator** — ❌ Fatal Error", state="error")
            st.error(f"Generation failed: {e}")
            st.stop()

        # 6. Action
        try:
            with st.status("⚡ **Agent 6: Action Simulator** — Executing downstream integrations...", expanded=True) as s:
                t0 = time.time()
                action_result = simulate_actions(state["generation"])
                elapsed = time.time() - t0
                if "error" in action_result:
                    raise RuntimeError(action_result["error"])
                state["action"] = action_result
                trace["action"] = {"output": action_result, "time_s": round(elapsed, 2)}
                triggered = sum(1 for v in action_result.values() if isinstance(v, str) and v.lower() not in ["skipped", "n/a", "none", "no", "false"])
                s.update(label=f"⚡ **Agent 6: Action Simulator** — ✔ Simulated {triggered} API integrations ({elapsed:.1f}s)", state="complete", expanded=False)
        except Exception as e:
            s.update(label="⚡ **Agent 6: Action Simulator** — ❌ Fatal Error", state="error")
            st.error(f"Action failed: {e}")
            st.stop()

        total_time = time.time() - pipeline_start

        # Save to session state
        st.session_state["pipeline_result"] = state
        st.session_state["agent_trace"] = trace
        st.session_state["workflow_history"].append({
            "task": user_task,
            "employee": emp_name,
            "role": emp_role,
            "score": state.get("compliance", {}).get("compliance_score", "N/A"),
            "time_s": round(total_time, 1),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

        st.success(f"🎉 **Pipeline Execution Successful** in {total_time:.1f} seconds. Review results below.")

    # ── Results Presentation ─────────────────────────────────────────
    if st.session_state["pipeline_result"]:
        result = st.session_state["pipeline_result"]
        compliance = result.get("compliance", {})
        generation = result.get("generation", {})
        action = result.get("action", {})
        planner = result.get("planner", {})

        st.markdown("---")
        st.markdown("### 📊 Workflow Audit Results")

        # ── Metric Cards ─────────────────────────────────────────────
        score = compliance.get("compliance_score", 0)
        try:
            score_val = int(score)
        except (ValueError, TypeError):
            score_val = 0

        num_tasks = len(planner.get("tasks", []))
        num_warnings = len(compliance.get("warnings", [])) + len(compliance.get("missing_requirements", []))
        triggered = sum(1 for v in action.values() if isinstance(v, str) and v.lower() not in ["skipped", "n/a", "none", "no", "false"])

        st.markdown('<div class="metric-row">', unsafe_allow_html=True)
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{num_tasks}</div><div class="metric-label">Tasks Planned</div></div>', unsafe_allow_html=True)
        with col_m2:
            score_color = "#16a34a" if score_val >= 80 else ("#ca8a04" if score_val >= 50 else "#dc2626")
            st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: {score_color};">{score_val}%</div><div class="metric-label">Compliance Score</div></div>', unsafe_allow_html=True)
        with col_m3:
            warn_color = "#dc2626" if num_warnings > 0 else "#64748b"
            st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: {warn_color};">{num_warnings}</div><div class="metric-label">Policy Warnings</div></div>', unsafe_allow_html=True)
        with col_m4:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{triggered}</div><div class="metric-label">System Triggers</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Warnings Box ─────────────────────────────────────────────
        warnings = compliance.get("warnings", [])
        missing = compliance.get("missing_requirements", [])
        if warnings or missing:
            warning_html = '<div class="warning-box"><strong>⚠️ Compliance Attention Required</strong>'
            warning_html += '<p style="margin-bottom: 0.5rem; font-size: 0.9rem;">The Reasoning Agent missed or violated the following policies. The Document Generator has automatically corrected these issues in the final packet.</p><ul>'
            for w in warnings:
                warning_html += f"<li><b>Violation:</b> {w}</li>"
            for m in missing:
                warning_html += f"<li><b>Missing Requirement:</b> {m}</li>"
            warning_html += "</ul></div>"
            st.markdown(warning_html, unsafe_allow_html=True)
        elif score_val == 100:
            st.success("✅ **Perfect Compliance:** The AI's strategic plan matched corporate policy with 100% accuracy. No warnings generated.")

        # ── Document Previews (Dynamic) ──────────────────────────────
        st.markdown("### 📄 Generated Corporate Documents")
        st.caption("These artifacts were dynamically generated and self-corrected based on the compliance audit.")
        
        doc_titles = [
            generation.get("doc_1_title", "Document 1"),
            generation.get("doc_2_title", "Document 2"),
            generation.get("doc_3_title", "Document 3"),
            generation.get("doc_4_title", "Document 4"),
        ]
        doc_contents = [
            generation.get("doc_1_md", "*No content*"),
            generation.get("doc_2_md", "*No content*"),
            generation.get("doc_3_md", "*No content*"),
            generation.get("doc_4_md", "*No content*"),
        ]
        
        tabs = st.tabs(doc_titles)
        for i, tab in enumerate(tabs):
            with tab:
                st.markdown(f'<div class="doc-preview">{doc_contents[i]}</div>', unsafe_allow_html=True)

        # ── Action Simulation Results (Dynamic) ──────────────────────
        st.markdown("### ⚡ Simulated Enterprise API Triggers")
        st.caption("In a production environment, these actions would fire webhooks to Jira, Workday, Slack, etc.")
        
        action_items = [(k.replace('_', ' ').title(), v) for k, v in action.items() if k not in ("error", "timestamp")]
        
        if not action_items:
            st.info("No downstream actions triggered.")
        else:
            col_a1, col_a2 = st.columns(2)
            for i, (label, status) in enumerate(action_items):
                col = col_a1 if i % 2 == 0 else col_a2
                status_str = str(status).lower()
                
                if status_str in ["ready", "completed", "success"]:
                    icon = "✅"
                elif status_str in ["submitted", "created", "sent", "processing"]:
                    icon = "🚀"
                elif status_str in ["skipped", "n/a", "none", "no", "false"]:
                    icon = "⏭️"
                else:
                    icon = "⏳"
                    
                html = f"""
                <div class="action-item">
                    <span class="action-icon">{icon}</span>
                    <span class="action-label">{label}</span>
                    <span class="action-status">{status_str.upper()}</span>
                </div>
                """
                col.markdown(html, unsafe_allow_html=True)

        # ── PDF Download ─────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        pdf_path = result.get("pdf_path")
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            st.download_button(
                label="📥 Download Complete Verified PDF Packet",
                data=pdf_data,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )


# ══════════════════════════════════════════════════════════════════════
# TAB 2: POLICY Q&A CHAT
# ══════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("### 💬 Corporate Knowledge Base Q&A")
    st.caption(
        "Chat securely with your uploaded documents using Retrieval-Augmented Generation (RAG). The AI cannot hallucinate outside of your policies."
    )

    if not index_exists():
        st.info("📄 Upload policy PDFs in the sidebar and build the knowledge base to activate chat.")
    else:
        # Display chat history
        for msg in st.session_state["chat_messages"]:
            css_class = "chat-user" if msg["role"] == "user" else "chat-ai"
            st.markdown(f'<div class="{css_class}"><strong>{"You" if msg["role"] == "user" else "PolicyPilot AI"}:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

        # Chat input
        if prompt := st.chat_input("e.g., What is our policy on remote employee hardware returns?"):
            st.session_state["chat_messages"].append({"role": "user", "content": prompt})
            st.markdown(f'<div class="chat-user"><strong>You:</strong><br>{prompt}</div>', unsafe_allow_html=True)

            with st.spinner("Searching corporate policies..."):
                # Retrieve relevant chunks
                results = retrieve(prompt, k=5)
                context = format_context(results)

                # Build the LLM prompt
                from utils.helpers import call_gemini_json
                from utils.gemini_client import get_chat_llm
                from langchain_core.messages import HumanMessage, SystemMessage

                llm = get_chat_llm(temperature=0.2)
                system = (
                    "You are PolicyPilot AI, an expert corporate policy assistant. "
                    "Answer the user's question based strictly on the provided policy excerpts. "
                    "If the answer is not in the excerpts, clearly state that the policy does not cover it. "
                    "Use professional, clear language and bullet points where appropriate."
                )
                user_msg = (
                    f"## Policy Excerpts\n{context}\n\n"
                    f"## User Question\n{prompt}"
                )

                try:
                    response = llm.invoke([
                        SystemMessage(content=system),
                        HumanMessage(content=user_msg),
                    ])
                    answer = response.content
                except Exception as e:
                    answer = f"Error generating response: {e}"

            st.markdown(f'<div class="chat-ai"><strong>PolicyPilot AI:</strong><br>{answer}</div>', unsafe_allow_html=True)

            # Show sources in an expander
            if results:
                with st.expander("📚 View Document Sources", expanded=False):
                    for i, r in enumerate(results, 1):
                        st.markdown(f"**Source {i}:** `{r['source']}` (Page {r['page']})")
                        st.caption(f"Relevance Score: {r['score']:.4f}")
                        st.markdown(f"> *{r['text']}*")
                        st.divider()

            st.session_state["chat_messages"].append({"role": "assistant", "content": answer})


# ══════════════════════════════════════════════════════════════════════
# TAB 3: WORKFLOW HISTORY
# ══════════════════════════════════════════════════════════════════════
with tab_history:
    st.markdown("### 📜 Session Execution Log")
    st.caption("A chronological audit trail of all automated workflows run during this session.")

    history = st.session_state["workflow_history"]
    if not history:
        st.info("No workflows have been executed yet. Return to the Launch Workflow tab to begin.")
    else:
        for i, run in enumerate(reversed(history), 1):
            score = run.get("score", "N/A")
            try:
                score_int = int(score)
                badge = "badge-excellent" if score_int >= 80 else ("badge-warning" if score_int >= 50 else "badge-danger")
            except (ValueError, TypeError):
                badge = "badge-warning"
                score_int = 0

            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-header">Execution #{len(history) - i + 1}</div>
                    <div style="margin-bottom: 0.5rem; color: #334155;"><strong>Task:</strong> {run['task']}</div>
                    <div class="timeline-meta">
                        👤 Target: <strong>{run['employee']}</strong> ({run['role']}) &nbsp;|&nbsp;
                        🛡️ Compliance: <span class="{badge}">{score}/100</span> &nbsp;|&nbsp;
                        ⏱️ Duration: {run['time_s']}s &nbsp;|&nbsp;
                        🕐 {run['timestamp']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════════
# TAB 4: AGENT TRACE / DEBUG
# ══════════════════════════════════════════════════════════════════════
with tab_trace:
    st.markdown("### 🔍 Multi-Agent Architecture Trace")
    st.caption(
        "Inspect the raw JSON payloads passed between agents in the most recent pipeline run. "
        "This transparency layer demonstrates exactly how the AI reasoned through your policies."
    )

    trace = st.session_state.get("agent_trace", {})
    if not trace:
        st.info("Execute a workflow to generate architectural trace data.")
    else:
        agents_info = [
            ("🗓️ Agent 1: Task Planner", "planner"),
            ("🔍 Agent 2: Policy Retriever", "retrieval"),
            ("🧠 Agent 3: Reasoner", "reasoning"),
            ("✅ Agent 4: Compliance Auditor", "compliance"),
            ("📝 Agent 5: Document Generator", "generator"),
            ("⚡ Agent 6: Action Simulator", "action"),
        ]

        for label, key in agents_info:
            data = trace.get(key)
            if data:
                elapsed = data.get("time_s", "N/A")
                with st.expander(f"{label} — ⏱️ {elapsed}s", expanded=False):
                    st.json(data)
            else:
                with st.expander(f"{label} — ⏳ No trace data generated", expanded=False):
                    pass
