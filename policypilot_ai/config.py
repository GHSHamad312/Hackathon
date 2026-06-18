"""
Centralised configuration for PolicyPilot AI.

Loads settings from a .env file (if present) via python-dotenv,
then reads environment variables with sensible defaults so the app
never crashes on a missing value — it will surface a clear Streamlit
warning instead.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env from the project root ─────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(_PROJECT_ROOT / ".env")

def get_secret(key: str, default: str | None = None) -> str | None:
    """Fetch API key with priority: runtime session key → st.secrets → env var."""
    try:
        import streamlit as st
        # 1) Runtime key entered by the user in the UI (highest priority)
        if key == "GOOGLE_API_KEY":
            runtime_key = st.session_state.get("temp_api_key", "")
            if runtime_key and runtime_key.strip():
                return runtime_key.strip()
        # 2) Streamlit Cloud secrets
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    # 3) .env / OS environment variable
    return os.getenv(key, default)

def __getattr__(name: str):
    if name == "GOOGLE_API_KEY":
        return get_secret("GOOGLE_API_KEY")
    if name == "CHAT_MODEL":
        return get_secret("CHAT_MODEL", "gemini-2.5-flash")
    if name == "EMBEDDING_MODEL":
        return get_secret("EMBEDDING_MODEL", "gemini-embedding-001")
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# ── Derived paths ────────────────────────────────────────────────────
SAMPLE_DOCS_DIR: Path = _PROJECT_ROOT / "sample_docs"
UPLOADED_DOCS_DIR: Path = _PROJECT_ROOT / "uploaded_docs"
OUTPUTS_DIR: Path = _PROJECT_ROOT / "outputs"
VECTORSTORE_DIR: Path = _PROJECT_ROOT / "vectorstore_data"

# Ensure runtime directories exist
for _dir in (SAMPLE_DOCS_DIR, UPLOADED_DOCS_DIR, OUTPUTS_DIR, VECTORSTORE_DIR):
    _dir.mkdir(parents=True, exist_ok=True)


def api_key_is_set() -> bool:
    """Return True when a non-empty API key is available."""
    key = get_secret("GOOGLE_API_KEY")
    return bool(key and key.strip()
                and key != "your-google-api-key-here" and key != "your_api_key_here")
