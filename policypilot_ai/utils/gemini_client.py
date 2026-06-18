"""
Shared Gemini client configuration.

Every module in the project should import from here instead of
initialising its own google-genai or langchain-google-genai
instances.  The API key is read once from config.py — it is **never**
hardcoded in this file or anywhere else.
"""

from __future__ import annotations

from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

import config
# ── Configure the low-level SDK lazily ─────────────────────────────
_client: genai.Client | None = None

def get_genai_client() -> genai.Client:
    """Return the shared google-genai Client instance."""
    global _client
    if _client is None and config.api_key_is_set():
        _client = genai.Client(api_key=config.GOOGLE_API_KEY)
        
    if _client is None:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. "
            "Add it to your .env file (see .env.example)."
        )
    return _client


def get_chat_llm(**kwargs) -> ChatGoogleGenerativeAI:
    """Return a LangChain chat model backed by Google Gemini.

    Raises RuntimeError when the API key is missing so callers can
    surface a friendly message rather than a cryptic traceback.
    """
    if not config.api_key_is_set():
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. "
            "Add it to your .env file (see .env.example)."
        )
    defaults = {
        "model": config.CHAT_MODEL,
        "google_api_key": config.GOOGLE_API_KEY,
        "temperature": 0.3,
        "convert_system_message_to_human": True,
    }
    defaults.update(kwargs)
    return ChatGoogleGenerativeAI(**defaults)


def get_embeddings(**kwargs) -> GoogleGenerativeAIEmbeddings:
    """Return a LangChain embeddings wrapper for Google Gemini."""
    if not config.api_key_is_set():
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. "
            "Add it to your .env file (see .env.example)."
        )
    defaults = {
        "model": f"models/{config.EMBEDDING_MODEL}",
        "google_api_key": config.GOOGLE_API_KEY,
    }
    defaults.update(kwargs)
    return GoogleGenerativeAIEmbeddings(**defaults)
