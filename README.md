# Pre-Meeting Briefing Agent

An AI research agent that takes a company or person and a meeting time, then produces a one-page, source-backed briefing covering the last 30 days. Built for the Global AI Hackathon (Problem Statement 05).

## Features
- Searches the last 30 days of news, launches, partnerships and hires using Tavily
- Generates a concise one-page briefing with an LLM routed through Bifrost
- Cites a numbered source for every factual claim
- Separates verified findings from an "Unverified / Unclear" section
- Suggests questions to ask in the meeting
- Streamlit UI with a downloadable Markdown briefing

## How it works
1. `researcher.py` runs several Tavily searches (news, launches, leadership) limited to 30 days and removes duplicate URLs.
2. `briefing.py` numbers the sources and sends them to the LLM with strict rules: use only the provided sources, cite every claim, never invent facts.
3. `llm_client.py` sends the request through an OpenAI-compatible endpoint (Bifrost gateway or any compatible provider).
4. `app.py` provides the Streamlit interface.

## Project structure
```
pre-meeting-briefing-agent/
├── app.py
├── requirements.txt
├── .env.example
└── src/
    ├── config.py
    ├── llm_client.py
    ├── researcher.py
    └── briefing.py
```

## Setup
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your keys:
```
TAVILY_API_KEY=your_tavily_key
LLM_API_KEY=your_llm_key
LLM_BASE_URL=http://localhost:8080/openai/v1
LLM_MODEL=openai/gpt-4o-mini
```

## Usage
Command line:
```powershell
python -m src.briefing "Nebius" "2026-11-16 10:00"
```

Web UI:
```powershell
streamlit run app.py
```

## Reliability
- Only sources from the last 30 days are used.
- The model is instructed to cite every claim and never invent facts.
- Anything it cannot support goes under "Unverified / Unclear".
- Every briefing ends with a clickable source list so the user can verify it.

## Tech stack
Python, Streamlit, Tavily (search), Bifrost (LLM gateway), OpenAI-compatible API