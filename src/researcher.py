from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

from tavily import TavilyClient

from . import config

WINDOW_DAYS = 30
MAX_SOURCES = 12


def _parse_date(value):
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _search(client, query, topic, n):
    kwargs = {"query": query, "max_results": n, "search_depth": "advanced", "topic": topic}
    if topic == "news":
        kwargs["days"] = WINDOW_DAYS
    else:
        kwargs["time_range"] = "month"
    return client.search(**kwargs).get("results", [])


def research(subject: str, max_results: int = 6) -> list[dict]:
    """Search the last 30 days from several angles. Returns deduped, dated sources."""
    client = TavilyClient(api_key=config.TAVILY_API_KEY)
    queries = [
        f'"{subject}" latest news',
        f'"{subject}" announcement launch partnership funding',
        f'"{subject}" appointed hires leadership executive',
    ]
    cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS + 1)
    seen, sources, errors = set(), [], []

    def add(results):
        for r in results:
            url = r.get("url")
            if not url or url in seen:
                continue
            dt = _parse_date(r.get("published_date"))
            if dt and dt < cutoff:
                continue  # enforce the 30-day window ourselves
            seen.add(url)
            sources.append({
                "title": (r.get("title") or "Untitled").strip(),
                "url": url,
                "content": (r.get("content") or "")[:500],
                "date": dt.strftime("%Y-%m-%d") if dt else "date unknown",
                "_dt": dt,
            })

    for q in queries:
        try:
            add(_search(client, q, "news", max_results))
        except Exception as e:
            errors.append(str(e))

    if len(sources) < 4:  # thin news coverage: widen to general web, still last month
        for q in queries[:2]:
            try:
                add(_search(client, q, "general", max_results))
            except Exception as e:
                errors.append(str(e))

    if not sources and errors:
        raise RuntimeError(f"Tavily search failed: {errors[0]}")

    floor = datetime.min.replace(tzinfo=timezone.utc)
    sources.sort(key=lambda s: s["_dt"] or floor, reverse=True)
    for s in sources:
        s.pop("_dt", None)
    return sources[:MAX_SOURCES]