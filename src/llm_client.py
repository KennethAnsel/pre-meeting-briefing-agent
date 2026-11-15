import time

from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError

from . import config


def _call(api_key, base_url, model, system, user):
    client = OpenAI(api_key=api_key, base_url=base_url, timeout=60, max_retries=0)
    resp = client.chat.completions.create(
        model=model,
        temperature=0.2,
        max_tokens=3000,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    text = resp.choices[0].message.content or ""
    if not text.strip():
        raise RuntimeError("Model returned an empty answer (raise max_tokens or pick another model)")
    return text


def chat(system: str, user: str) -> str:
    targets = [(config.LLM_API_KEY, config.LLM_BASE_URL, config.LLM_MODEL)]
    if config.FALLBACK_API_KEY and config.FALLBACK_BASE_URL and config.FALLBACK_MODEL:
        targets.append((config.FALLBACK_API_KEY, config.FALLBACK_BASE_URL, config.FALLBACK_MODEL))

    last_error = None
    for api_key, base_url, model in targets:
        for attempt in range(3):
            try:
                return _call(api_key, base_url, model, system, user)
            except RateLimitError as e:  # free tiers rate-limit: wait and retry
                last_error = e
                time.sleep(3 * (attempt + 1))
            except APIConnectionError as e:  # endpoint down: go to next target
                last_error = e
                break
            except APIStatusError as e:
                last_error = e
                if e.status_code >= 500:
                    time.sleep(2)
                    continue
                break  # 401/404 etc: retrying will not help
    raise RuntimeError(f"LLM request failed: {last_error}")