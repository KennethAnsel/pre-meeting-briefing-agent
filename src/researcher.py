from tavily import TavilyClient
from .config import TAVILY_API_KEY


def research(subject: str, max_results: int = 6) -> list[dict]:
    """Search the last 30 days from several angles. Returns deduped sources."""
    client = TavilyClient(api_key=TAVILY_API_KEY)
    queries = [
        f"{subject} latest news",
        f"{subject} product launch partnership funding announcement",
        f"{subject} new hire leadership change executive",
    ]
    seen, sources = set(), []
    for q in queries:
        res = client.search(
            query=q,
            topic="news",
            days=30,
            max_results=max_results,
            search_depth="advanced",
        )
        for r in res.get("results", []):
            url = r.get("url")
            if not url or url in seen:
                continue
            seen.add(url)
            sources.append({
                "title": r.get("title", ""),
                "url": url,
                "content": (r.get("content") or "")[:700],
                "date": r.get("published_date", "unknown"),
            })
    return sources