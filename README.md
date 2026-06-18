<p align="center">
  <img src="https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white" alt="FAISS"/>
</p>

<h1 align="center">✈️ PolicyPilot AI</h1>

<p align="center">
  <b>The Autonomous Compliance & Workflow Engine for Modern Enterprises</b><br/>
  <sub>Built at AI Hackathon 2026 — Powered by a 6-Agent Agentic Architecture & RAG over Company Policies</sub>
</p>

<p align="center">
  <a href="#-what-it-does">What It Does</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-team">Team</a>
</p>

---

## 🎯 What It Does

PolicyPilot AI is an **enterprise-grade AI assistant** that fully automates HR and operations workflows — such as employee onboarding, offboarding, and compliance audits — by combining a **multi-agent pipeline** with **Retrieval-Augmented Generation (RAG)** over your company's actual PDF policies.

> **Upload your company policies → Tell it what to do → Get a fully compliant, audited document packet in seconds.**

### ✨ Key Highlights

| Feature | Description |
|---|---|
| 🤖 **6-Agent Pipeline** | Planner → Retriever → Reasoner → Compliance Auditor → Generator → Action Simulator |
| 📄 **RAG over PDFs** | Upload any HR/IT/SOP documents — the AI grounds every decision in your actual policies |
| 🛡️ **Compliance Scoring** | Automatic audit with a 0–100 compliance score, warnings, and missing requirement detection |
| 📝 **Auto-Generated Docs** | Produces 4 tailored corporate documents (checklists, emails, memos) per workflow |
| 💬 **Policy Q&A Chat** | Chat with your policies using RAG — no hallucination outside your documents |
| 📥 **PDF Export** | One-click download of the complete verified document packet |

---

## 🏗️ Architecture

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                    POLICYPILOT AI ENGINE                     │
│                                                             │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐             │
│  │  Planner  │──▶│ Retriever │──▶│ Reasoner  │             │
│  │  Agent    │   │  Agent    │   │  Agent    │             │
│  └───────────┘   └─────┬─────┘   └─────┬─────┘             │
│                        │               │                    │
│                  ┌─────▼─────┐   ┌─────▼──────┐            │
│                  │   FAISS   │   │ Compliance  │            │
│                  │  Vector   │   │  Auditor    │            │
│                  │   Store   │   │  Agent      │            │
│                  └───────────┘   └─────┬──────┘            │
│                                        │                    │
│                  ┌─────────────┐ ┌─────▼──────┐            │
│                  │   Action    │◀│ Generator   │            │
│                  │  Simulator  │ │   Agent     │            │
│                  └─────────────┘ └────────────┘            │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
Compliant Documents + Compliance Report + PDF Packet
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/policypilot-ai.git
cd policypilot-ai/policypilot_ai

# 2. Install dependencies
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Add your Gemini API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Launch
streamlit run app.py
```

> 📖 **See the [detailed README inside `policypilot_ai/`](./policypilot_ai/README.md)** for full documentation, architecture deep-dives, and usage guides.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit (custom CSS, animated gradients) |
| **LLM & Embeddings** | Google Gemini 2.5 Flash (`langchain-google-genai`) |
| **Orchestration** | LangChain v1.x |
| **Vector Store** | FAISS (CPU) |
| **Document Processing** | pypdf + RecursiveCharacterTextSplitter |
| **PDF Generation** | ReportLab |

---

## 👥 Team

Built at **Atomcamp AI Hackathon 2026 at buitems** by:

| Name | Role |
|---|---|
| **Hamad Ali Shah** | Developer |
| **Sameer Talreja** | Developer |
| **Naeem Ahmed** | Developer |

---

<p align="center">
  <sub>Made with 🤖 Google Gemini · 🦜 LangChain · 🎈 Streamlit</sub>
</p>
