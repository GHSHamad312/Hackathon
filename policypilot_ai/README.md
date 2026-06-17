# PolicyPilot AI ✈️

PolicyPilot AI is an enterprise assistant that automates HR and operations workflows (such as employee onboarding) by combining a multi-agent pipeline with Retrieval-Augmented Generation (RAG) over uploaded company PDFs. 

Built with **Streamlit**, **LangChain**, and **Google Gemini 2.5 Flash**, PolicyPilot acts as an intelligent AI employee that understands your company's internal policies and actively drafts, plans, and validates operational tasks.

---

## 🏗️ Architecture

PolicyPilot AI operates using a sequential multi-agent architecture. When a user submits a task (e.g., *"Onboard Ahmed as a Software Engineer"*), the system orchestrates the following flow:

1. **Planner Agent**: Decomposes the high-level request into an ordered, structured list of necessary sub-tasks.
2. **Retrieval Agent (RAG)**: Takes the planner's tasks and queries a local **FAISS** vector store built from uploaded PDFs (e.g., HR Policies, SOPs, IT Asset rules) to extract highly relevant context.
3. **Reasoning Agent**: Synthesizes the extracted policy passages against the planner's tasks to identify required actions, dependencies, and necessary documents (e.g., catching that an NDA is strictly required for onboarding).
4. **Compliance Agent**: Acts as an internal auditor, comparing the reasoning output against the raw policies to identify any missing steps, generating a compliance score and warning flags.
5. **Generator Agent**: Drafts polished Markdown documents (Onboarding Checklists, Welcome Emails, Manager Summaries) and renders them into a downloadable PDF via `reportlab`.
6. **Action Agent**: Simulates downstream enterprise integrations (e.g., Jira IT tickets, automated HR emails).

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.11+
- A Google Gemini API Key

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/policypilot-ai.git
cd policypilot-ai
```

### 2. Install dependencies
It is highly recommended to use a virtual environment.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Get a Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Create a new project and generate a free API Key.
3. Rename the `.env.example` file to `.env` (or create a new `.env` file).
4. Add your API key:
```env
GOOGLE_API_KEY=your-actual-api-key-here
```
*(Note: You can also paste the API key directly into the Streamlit sidebar during runtime if you prefer not to save it to disk).*

---

## 🎮 Running the Application

To start the local Streamlit server:
```bash
streamlit run app.py
```
This will open the application in your default web browser (usually at `http://localhost:8504`).

### Generating Sample Data (Optional)
If you don't have company PDFs on hand to test the RAG capabilities, we have provided a script to generate realistic sample documents (HR Policy, IT Asset Policy, Onboarding SOP):
```bash
python generate_samples.py
```
This will create three PDF files in the `sample_docs/` folder which you can upload directly into the Streamlit UI.

---

## 💡 How to use the UI
1. **Upload Documents**: Use the sidebar to upload your company PDFs (e.g., the ones generated in `sample_docs/`).
2. **Build Knowledge Base**: Click the blue button in the sidebar to extract, chunk, embed, and index the PDFs into the FAISS vector store.
3. **Run Workflow**: In the main area, fill in an employee name (e.g., *Ahmed*), role (e.g., *Software Engineer*), and workflow task. Click **Run Workflow**.
4. **View Results**: Watch the agents execute live. Once finished, you'll see a compliance score, Markdown previews, and a button to download the finalized onboarding PDF packet.

---

## 🛠️ Technology Stack
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Orchestration**: [LangChain (v1.x)](https://python.langchain.com/)
- **LLM & Embeddings**: Google Gemini (`google-genai` / `langchain-google-genai`)
- **Vector Store**: [FAISS](https://github.com/facebookresearch/faiss) (CPU)
- **Document Processing**: `pypdf`, LangChain `RecursiveCharacterTextSplitter`
- **PDF Generation**: `reportlab`
