import os
from dotenv import load_dotenv

# override=True: values in .env win over stale system environment variables
load_dotenv(override=True)


def _get(name, default=""):
    return os.getenv(name, default).strip().strip('"').strip("'")


TAVILY_API_KEY = _get("TAVILY_API_KEY")
LLM_API_KEY = _get("LLM_API_KEY")
LLM_BASE_URL = _get("LLM_BASE_URL", "https://api.groq.com/openai/v1")
LLM_MODEL = _get("LLM_MODEL", "llama-3.1-8b-instant")

# Optional: used automatically if the primary endpoint (e.g. Bifrost) is unreachable
FALLBACK_API_KEY = _get("FALLBACK_API_KEY")
FALLBACK_BASE_URL = _get("FALLBACK_BASE_URL")
FALLBACK_MODEL = _get("FALLBACK_MODEL")


def _is_placeholder(value):
    low = value.lower()
    return (not value) or any(t in low for t in ("your", "xxxx", "the_long_key", "placeholder"))


def check_config():
    """Return a list of human-readable setup problems (empty list = OK)."""
    problems = []
    if _is_placeholder(TAVILY_API_KEY):
        problems.append("TAVILY_API_KEY is missing or still a placeholder in .env")
    elif not TAVILY_API_KEY.startswith("tvly-"):
        problems.append("TAVILY_API_KEY should start with 'tvly-'")
    if _is_placeholder(LLM_API_KEY):
        problems.append("LLM_API_KEY is missing or still a placeholder in .env")
    if not LLM_BASE_URL:
        problems.append("LLM_BASE_URL is missing in .env")
    if not LLM_MODEL:
        problems.append("LLM_MODEL is missing in .env")
    return problems