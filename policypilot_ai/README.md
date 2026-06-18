<p align="center">
  <img src="https://img.shields.io/badge/Google_Gemini_2.5_Flash-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/LangChain_v1-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FAISS_CPU-0467DF?style=for-the-badge&logo=meta&logoColor=white" alt="FAISS"/>
  <img src="https://img.shields.io/badge/ReportLab-2C2D72?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="ReportLab"/>
</p>

<h1 align="center">✈️ PolicyPilot AI</h1>

<p align="center">
  <b>The Autonomous Compliance & Workflow Engine for Modern Enterprises</b>
</p>

<p align="center">
  <b>Online at https://policypilotai-rn8aekmr5wsglf9qzk7gxh.streamlit.app/</b>
</p>

<p align="center">
  <sub>An AI-powered enterprise assistant that automates HR & operations workflows using a 6-agent agentic architecture with Retrieval-Augmented Generation (RAG) over your company's actual policy documents.</sub>
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-features">Features</a> •
  <a href="#-architecture-deep-dive">Architecture</a> •
  <a href="#-project-structure">Project Structure</a> •
  <a href="#-setup--installation">Setup</a> •
  <a href="#-usage-guide">Usage</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-testing">Testing</a> •
  <a href="#-team">Team</a>
</p>

---

## 📋 Overview

**PolicyPilot AI** is an enterprise-grade intelligent assistant that transforms how organizations handle HR and operational workflows. Instead of manually cross-referencing policy documents, drafting checklists, and auditing for compliance — PolicyPilot does it all autonomously in seconds.

### The Problem

Enterprise HR and operations teams spend hours on repetitive workflows:
- 📑 Manually reading through 50+ page policy documents
- ✅ Creating onboarding/offboarding checklists from scratch
- 🔍 Cross-checking every step against compliance requirements
- 📧 Drafting welcome emails, manager briefings, IT tickets
- ⚠️ Risking compliance violations from human error

### Our Solution

**Upload your company policies → Describe the task → Get a fully compliant, audited document packet in seconds.**

PolicyPilot AI deploys a team of 6 specialized AI agents that work together in a sequential pipeline, each one building on the previous agent's output — just like a real enterprise operations team, but executing in under 30 seconds.

---

## ✨ Features

### 🤖 Core Capabilities

| Feature | Description |
|:---|:---|
| **Multi-Agent Pipeline** | 6 specialized AI agents execute in sequence: Plan → Retrieve → Reason → Audit → Generate → Act |
| **RAG-Powered Intelligence** | Every decision is grounded in your actual company policies via FAISS vector similarity search |
| **Compliance Auditing** | Automatic 0–100 compliance scoring with detailed warnings and missing requirement detection |
| **Dynamic Document Generation** | Produces 4 tailored corporate documents per workflow (checklists, emails, summaries, memos) |
| **Self-Correction Loop** | The Generator Agent automatically injects missing requirements flagged by the Compliance Auditor |
| **PDF Export** | One-click download of the complete verified document packet via ReportLab |

### 💬 Interactive Features

| Feature | Description |
|:---|:---|
| **Policy Q&A Chat** | RAG-powered chatbot that answers questions strictly from your uploaded policies — zero hallucination |
| **Agent Trace Inspector** | Full transparency layer showing raw JSON payloads between every agent in the pipeline |
| **Execution History** | Chronological audit trail of all workflows with compliance scores, timings, and metadata |
| **Live Pipeline Status** | Real-time progress indicators as each agent executes with timing breakdowns |

### 🎨 Enterprise UI

| Feature | Description |
|:---|:---|
| **Animated Hero Header** | Gradient header with shimmer animation and glassmorphism badges |
| **Metric Dashboard** | Real-time cards showing tasks planned, compliance score, warnings, and system triggers |
| **Dynamic Workflow Types** | Pre-configured templates for Onboarding, Offboarding, Transfers, PIP, Leave, Compliance Audits |
| **Responsive Layout** | Wide-layout Streamlit app with custom CSS, hover effects, and professional styling |

---

## 🏗️ Architecture Deep Dive

PolicyPilot AI uses a **sequential multi-agent architecture** where each agent is a specialized module with a single responsibility. The agents communicate through structured JSON payloads, and the pipeline includes comprehensive error boundaries at every stage.

### Pipeline Flow

```
                         ╔══════════════════════════════════╗
                         ║        USER REQUEST              ║
                         ║  "Onboard Ahmed as a Software    ║
                         ║   Engineer"                      ║
                         ╚══════════════╤═══════════════════╝
                                        │
                    ┌───────────────────▼───────────────────┐
                    │        🗓️ AGENT 1: PLANNER             │
                    │                                       │
                    │  • Decomposes request into ordered     │
                    │    sub-tasks using Gemini              │
                    │  • Output: {goal, tasks[]}            │
                    └───────────────────┬───────────────────┘
                                        │
                    ┌───────────────────▼───────────────────┐
                    │      🔍 AGENT 2: RETRIEVER (RAG)       │
                    │                                       │
                    │  • Queries FAISS vector store for      │
                    │    each sub-task                       │
                    │  • Deduplicates passages               │
                    │  • Output: [{text, source, page,      │
                    │             score}]                    │
                    └───────────────────┬───────────────────┘
                                        │
                    ┌───────────────────▼───────────────────┐
                    │        🧠 AGENT 3: REASONER            │
                    │                                       │
                    │  • Synthesizes tasks + policy passages │
                    │  • Identifies required documents,      │
                    │    actions, dependencies               │
                    │  • Output: {summary, actions[],       │
                    │    required_documents[], departments[]}│
                    └───────────────────┬───────────────────┘
                                        │
                    ┌───────────────────▼───────────────────┐
                    │    ✅ AGENT 4: COMPLIANCE AUDITOR       │
                    │                                       │
                    │  • Cross-checks reasoning against raw  │
                    │    policy passages                     │
                    │  • Generates compliance score (0–100)  │
                    │  • Flags missing requirements & warns  │
                    │  • Output: {compliance_score,          │
                    │    warnings[], missing_requirements[], │
                    │    recommendations[]}                  │
                    └───────────────────┬───────────────────┘
                                        │
                    ┌───────────────────▼───────────────────┐
                    │      📝 AGENT 5: GENERATOR             │
                    │                                       │
                    │  • Drafts 4 dynamic Markdown documents │
                    │  • Self-corrects by injecting missing  │
                    │    requirements from compliance audit  │
                    │  • Exports to polished PDF via         │
                    │    ReportLab                           │
                    │  • Output: {doc_1_title, doc_1_md,     │
                    │    doc_2_title, doc_2_md, ...}         │
                    └───────────────────┬───────────────────┘
                                        │
                    ┌───────────────────▼───────────────────┐
                    │     ⚡ AGENT 6: ACTION SIMULATOR        │
                    │                                       │
                    │  • Simulates downstream enterprise     │
                    │    integrations (Jira, Slack, email)   │
                    │  • Dynamically determines which        │
                    │    actions to trigger based on docs    │
                    │  • Output: {jira_ticket: "created",   │
                    │    hr_email: "sent", ...}              │
                    └───────────────────┬───────────────────┘
                                        │
                         ╔══════════════▼═══════════════════╗
                         ║         FINAL OUTPUT             ║
                         ║                                  ║
                         ║  ✅ Compliance Score & Warnings   ║
                         ║  📄 4 Corporate Documents        ║
                         ║  📥 Downloadable PDF Packet      ║
                         ║  ⚡ Simulated API Triggers        ║
                         ╚══════════════════════════════════╝
```

### RAG Pipeline Detail

```
  PDF Upload                    Chunking                    Embedding & Indexing
┌──────────┐            ┌──────────────────┐            ┌───────────────────┐
│ HR Policy│            │ RecursiveChar    │            │ Google Gemini     │
│ IT Policy│──pypdf────▶│ TextSplitter     │───────────▶│ Embeddings        │
│ SOPs     │  extract   │ (800 chars,      │  vectorize │ (embedding-001)   │
│ ...      │  per-page  │  100 overlap)    │            │                   │
└──────────┘            └──────────────────┘            └────────┬──────────┘
                                                                 │
                                                          ┌──────▼──────┐
                             Similarity Search            │   FAISS     │
                User Query ─────────────────────────────▶ │   Vector    │
                             cosine similarity            │   Store     │
                             top-k results                │  (on disk)  │
                                                          └─────────────┘
```

---

## 📁 Project Structure

```
policypilot_ai/
│
├── app.py                      # 🎯 Main Streamlit application (884 lines)
│                                #    - Hero UI, sidebar, 4-tab layout
│                                #    - Pipeline orchestration with live status
│                                #    - Policy Q&A chat, history, agent trace
│
├── pipeline.py                 # 🔄 Headless pipeline orchestrator
│                                #    - Sequential agent execution with error boundaries
│                                #    - Returns partial results on failure
│
├── config.py                   # ⚙️ Centralized configuration
│                                #    - API key resolution (runtime → secrets → .env)
│                                #    - Model selection, directory paths
│
├── requirements.txt            # 📦 Python dependencies (9 packages)
├── runtime.txt                 # 🐍 Python version specification (3.11.9)
├── .env.example                # 🔐 Environment variable template
│
├── agents/                     # 🤖 Multi-Agent Modules
│   ├── __init__.py
│   ├── planner.py              #    Agent 1: Task decomposition
│   ├── retriever.py            #    Agent 2: FAISS vector search per task
│   ├── reasoning.py            #    Agent 3: Policy synthesis & action planning
│   ├── compliance.py           #    Agent 4: Compliance audit & scoring
│   ├── generator.py            #    Agent 5: Document drafting + PDF export
│   └── action.py               #    Agent 6: Enterprise action simulation
│
├── prompts/                    # 💬 LLM System Prompts
│   ├── __init__.py
│   ├── planner_prompt.py       #    Planner agent instructions
│   ├── reasoning_prompt.py     #    Reasoning agent instructions
│   ├── compliance_prompt.py    #    Compliance audit instructions
│   ├── generator_prompt.py     #    Document generation schema
│   └── action_prompt.py        #    Action simulation instructions
│
├── rag/                        # 📚 Retrieval-Augmented Generation
│   ├── __init__.py
│   ├── ingest.py               #    PDF extraction + chunking pipeline
│   ├── vectorstore.py          #    FAISS index build/load/save/clear
│   └── retrieval.py            #    Similarity search + context formatting
│
├── utils/                      # 🛠️ Shared Utilities
│   ├── __init__.py
│   ├── gemini_client.py        #    Centralized Gemini LLM & embedding config
│   ├── helpers.py              #    JSON parsing, retry logic, text utilities
│   └── pdf.py                  #    PDF utility functions
│
├── sample_docs/                # 📄 Sample Policy Documents (for testing)
│   ├── Acme_HR_Policy_2026.pdf
│   ├── Employee_Lifecycle_SOP_v4.pdf
│   └── IT_Asset_Security_Policy_v2.pdf
│
├── test_agents.py              # 🧪 Agent unit tests
├── test_pipeline.py            # 🧪 Pipeline integration tests
├── test_rag.py                 # 🧪 RAG system tests
├── simulate_ui_run.py          # 🖥️ CLI simulation of the full pipeline
│
├── uploaded_docs/              # 📤 User-uploaded PDFs (runtime)
├── outputs/                    # 📥 Generated PDF outputs (runtime)
├── vectorstore_data/           # 💾 Persisted FAISS index files (runtime)
│
└── .streamlit/
    └── config.toml             # 🎨 Streamlit theme configuration (teal/white)
```

---

## 🚀 Setup & Installation

### Prerequisites

| Requirement | Version |
|:---|:---|
| Python | 3.11+ |
| pip | Latest |
| Google Gemini API Key | Free from [Google AI Studio](https://aistudio.google.com/) |

### Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/policypilot-ai.git
cd policypilot-ai/policypilot_ai
```

### Step 2 — Create a Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary><b>📦 Full Dependency List</b></summary>

| Package | Version | Purpose |
|:---|:---|:---|
| `streamlit` | ≥1.45, <2.0 | Web application framework |
| `langchain` | ≥1.0, <2.0 | Agent orchestration framework |
| `langchain-community` | ≥0.3, <1.0 | Community integrations (FAISS) |
| `langchain-google-genai` | ≥4.0, <5.0 | Google Gemini LLM & embeddings |
| `google-genai` | ≥1.65, <3.0 | Google GenAI SDK |
| `faiss-cpu` | ≥1.9, <2.0 | Vector similarity search (CPU) |
| `pypdf` | ≥5.0, <6.0 | PDF text extraction |
| `python-dotenv` | ≥1.1, <2.0 | Environment variable loading |
| `reportlab` | ≥4.3, <5.0 | PDF document generation |

</details>

### Step 4 — Configure API Key

**Option A: Environment file (Recommended)**
```bash
cp .env.example .env
```
Edit `.env` and add your key:
```env
GOOGLE_API_KEY=your-actual-api-key-here
```

**Option B: Runtime input**
You can also paste your API key directly into the Streamlit sidebar at runtime. The key is stored in memory only and cleared when the session ends.

**Option C: Streamlit Cloud Secrets**
If deploying to Streamlit Cloud, add `GOOGLE_API_KEY` to your app's secrets.

### Step 5 — Launch the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501` (or `8504` depending on port availability).

---

## 🎮 Usage Guide

### 1. Upload Company Policies

Use the **sidebar** to upload your company's PDF documents:
- HR Policy manuals
- IT Asset & Security policies
- Standard Operating Procedures (SOPs)
- Employee handbooks
- Any compliance-relevant documents

> 💡 **Don't have documents?** We include 3 sample PDFs in `sample_docs/` — just upload those to try it out!

### 2. Build the Knowledge Base

Click **"Build Knowledge Base"** in the sidebar. PolicyPilot will:
1. Extract text from each PDF page-by-page using `pypdf`
2. Split text into overlapping chunks (800 chars, 100 overlap)
3. Embed chunks using Google Gemini's `embedding-001` model
4. Index embeddings in a FAISS vector store (persisted to disk)

### 3. Launch a Workflow

In the **"🚀 Launch Workflow"** tab:

1. **Select a workflow type** from 7 pre-configured templates:
   - Employee Onboarding
   - Employee Offboarding
   - Internal Role Transfer
   - Leave of Absence Processing
   - Performance Improvement Plan (PIP)
   - Policy Compliance Audit
   - Custom Task (free-form)

2. **Fill in subject details** — employee name and role/context

3. **Review/edit directives** — the system auto-generates task instructions, but you can customize them

4. **Click "Initialize Multi-Agent Pipeline"** — watch all 6 agents execute live with real-time status updates

### 4. Review Results

After pipeline completion, you'll see:

- **📊 Metric Dashboard** — Tasks planned, compliance score (color-coded), policy warnings, system triggers
- **⚠️ Compliance Warnings** — Detailed violation and missing requirement alerts
- **📄 Generated Documents** — 4 tabbed document previews with rich Markdown
- **⚡ Simulated Actions** — Enterprise API triggers (Jira, email, Slack, etc.)
- **📥 PDF Download** — Complete verified document packet

### 5. Chat with Your Policies

Switch to the **"💬 Policy Q&A"** tab to ask natural language questions:

```
"What is our policy on remote employee hardware returns?"
"How many days of probation are required for new hires?"
"What documents are needed for an internal transfer?"
```

The AI answers **strictly** from your uploaded policies — no hallucination.

### 6. Review History & Traces

- **📜 Execution History** — Chronological audit trail of all workflows with compliance scores
- **🔍 Architecture Trace** — Raw JSON payloads showing exactly how each agent reasoned

---

## ⚙️ How It Works

### Agent Communication Protocol

All agents communicate through **structured JSON**. Each agent module:
1. Receives input from the previous stage
2. Constructs a specialized prompt (from `prompts/`)
3. Calls Gemini via `utils/helpers.py::call_gemini_json()`
4. Returns a parsed JSON response (with automatic retry on parse failure)

### Defensive JSON Parsing

The `call_gemini_json()` utility implements a 2-attempt strategy:
1. **First attempt**: Send system + user prompt, parse response as JSON
2. **Retry on failure**: Append a stricter "return only JSON" instruction and retry
3. **Fallback**: If both attempts fail, return a safe fallback object (no crash)

This ensures the pipeline **never crashes** due to LLM formatting issues.

### Error Boundaries

The `pipeline.py` orchestrator wraps every stage in a `try/except` block. If any agent fails:
- The pipeline **halts gracefully**
- All partial results gathered up to that point are **preserved**
- The failure stage and error message are recorded in the state object

### API Key Resolution Priority

PolicyPilot resolves the Google API key with this priority chain:
1. **Runtime session key** (entered in the Streamlit sidebar — highest priority)
2. **Streamlit Cloud secrets** (`st.secrets["GOOGLE_API_KEY"]`)
3. **Environment variable** (`.env` file or OS-level `GOOGLE_API_KEY`)

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive web UI with custom CSS |
| **LLM** | [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) | Task decomposition, reasoning, generation |
| **Embeddings** | Google Gemini `embedding-001` | Semantic vector representations |
| **Orchestration** | [LangChain v1.x](https://python.langchain.com/) | Agent framework, text splitting, message protocols |
| **Vector Store** | [FAISS (CPU)](https://github.com/facebookresearch/faiss) | Fast similarity search over policy chunks |
| **PDF Extraction** | [pypdf](https://pypdf.readthedocs.io/) | Page-by-page text extraction from uploaded PDFs |
| **PDF Generation** | [ReportLab](https://www.reportlab.com/) | Professional PDF document creation with styling |
| **Config** | [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment variable management |

---

## 🧪 Testing

The project includes comprehensive test suites:

```bash
# Run all agent tests
python -m pytest test_agents.py -v

# Run pipeline integration tests
python -m pytest test_pipeline.py -v

# Run RAG system tests
python -m pytest test_rag.py -v

# Run the CLI simulation (no browser needed)
python simulate_ui_run.py
```

| Test File | Coverage |
|:---|:---|
| `test_agents.py` | Individual agent unit tests (planner, reasoning, compliance, generator, action) |
| `test_pipeline.py` | End-to-end pipeline integration tests |
| `test_rag.py` | PDF ingestion, chunking, vector store build/load, retrieval |
| `simulate_ui_run.py` | Full pipeline CLI simulation without Streamlit UI |

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|:---|:---|:---|:---|
| `GOOGLE_API_KEY` | ✅ Yes | — | Your Google Gemini API key |
| `CHAT_MODEL` | ❌ No | `gemini-2.5-flash` | LLM model for agent reasoning |
| `EMBEDDING_MODEL` | ❌ No | `gemini-embedding-001` | Model for text embeddings |

### Streamlit Theme

The app uses a custom teal-and-white theme defined in `.streamlit/config.toml`:

| Property | Value |
|:---|:---|
| Primary Color | `#008080` (Teal) |
| Background | `#F8F9FA` (Light Gray) |
| Secondary Background | `#FFFFFF` (White) |
| Text Color | `#1A2B4C` (Dark Navy) |
| Font | Sans Serif |

---

## 📄 Sample Documents

Three realistic enterprise policy PDFs are included in `sample_docs/` for immediate testing:

| Document | Description |
|:---|:---|
| `Acme_HR_Policy_2026.pdf` | Comprehensive HR policies (hiring, termination, leave, benefits) |
| `Employee_Lifecycle_SOP_v4.pdf` | Standard operating procedures for the full employee lifecycle |
| `IT_Asset_Security_Policy_v2.pdf` | IT asset management, security protocols, hardware provisioning |

These documents are designed to demonstrate the full power of the RAG pipeline and compliance auditing.

---

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. Push your repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your repo and select `policypilot_ai/app.py` as the entry point
4. Add `GOOGLE_API_KEY` to the app's **Secrets** section
5. Deploy — the `runtime.txt` ensures Python 3.11 is used

### Docker (DevContainer)

A `.devcontainer/devcontainer.json` is included for VS Code / GitHub Codespaces:
```bash
# Open in VS Code with Remote - Containers extension
# The container will auto-install all dependencies
```



## 👥 Team

Built with ❤️ at **AI Hackathon 2026** by:

<table>
  <tr>
    <td align="center"><b>Hamad Ali Shah</b><br/><sub>Developer</sub></td>
    <td align="center"><b>Sameer Talreja</b><br/><sub>Developer</sub></td>
    <td align="center"><b>Naeem Ahmed</b><br/><sub>Developer</sub></td>
  </tr>
</table>

---

## 📝 License

This project was built at the **Atomcamp AI Hackathon 2026**. Please contact the team for licensing inquiries.

---

<p align="center">
  <b>PolicyPilot AI</b> — Because compliance shouldn't be a bottleneck. ✈️
</p>

<p align="center">
  <sub>Powered by 🤖 Google Gemini 2.5 Flash · 🦜 LangChain · 🎈 Streamlit · 🔍 FAISS</sub>
</p>
