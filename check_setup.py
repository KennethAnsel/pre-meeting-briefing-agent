from src import config
from src.researcher import research
from src.llm_client import chat


def step(name, fn):
    try:
        print(f"[OK]   {name}: {fn()}")
        return True
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
        return False


def check_config():
    problems = config.check_config()
    if problems:
        raise RuntimeError("; ".join(problems))
    return f"model={config.LLM_MODEL} url={config.LLM_BASE_URL}"


if __name__ == "__main__":
    ok = step("Config (.env)", check_config)
    if ok:
        ok = step("Tavily search", lambda: f"{len(research('Tavily'))} recent sources")
    if ok:
        ok = step("LLM call", lambda: chat("Reply with the single word OK.", "ping").strip()[:40])
    print("\nAll good. Run: python -m streamlit run app.py" if ok else "\nFix the first [FAIL] above, then run again.")