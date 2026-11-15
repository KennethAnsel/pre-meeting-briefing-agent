import sys
from datetime import date

from .llm_client import chat
from .researcher import research

SYSTEM = """You are a meeting-prep analyst. Write a ONE-PAGE briefing (max ~350 words) in Markdown.
Rules:
- Use ONLY the numbered sources provided. Cite every factual claim like [1] or [2][3].
- Never invent facts, numbers, names or dates. If a claim is not clearly in a source, leave it out.
- Only include developments from the last 30 days. Sources marked 'date unknown' go under 'Unverified / Unclear'.
- Mark a bullet '(single source)' if it rests on only one source; claims backed by 2+ sources are verified.
- Tailor the meeting questions to the meeting type.
Sections, in this order:
## Snapshot (2 lines)
## Key developments (last 30 days) (bullets, each cited)
## People & leadership (only if sources support it, otherwise write 'No recent changes found.')
## Unverified / Unclear
## Questions to ask in the meeting (4-5 sharp questions)"""


def generate_briefing(subject: str, meeting_time: str, meeting_type: str = "General") -> str:
    sources = research(subject)
    if not sources:
        return f"No recent (30-day) sources found for **{subject}**. Try a more specific name."

    numbered = "\n\n".join(
        f"[{i}] {s['title']} ({s['date']})\n{s['url']}\n{s['content']}"
        for i, s in enumerate(sources, 1)
    )
    user = (
        f"Today: {date.today().isoformat()}\nSubject: {subject}\n"
        f"Meeting time: {meeting_time}\nMeeting type: {meeting_type}\n\nSOURCES:\n{numbered}"
    )
    body = chat(SYSTEM, user)
    refs = "\n".join(f"[{i}] [{s['title']}]({s['url']}) ({s['date']})" for i, s in enumerate(sources, 1))
    return (
        f"# Briefing: {subject}\n*Meeting: {meeting_time} | {meeting_type}*\n\n"
        f"{body}\n\n---\n## Sources\n{refs}"
    )


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    subject = sys.argv[1] if len(sys.argv) > 1 else "Tavily"
    when = sys.argv[2] if len(sys.argv) > 2 else "tomorrow 10:00"
    print(generate_briefing(subject, when))