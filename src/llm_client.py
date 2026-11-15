from openai import OpenAI
from .config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL


def chat(system: str, user: str) -> str:
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content