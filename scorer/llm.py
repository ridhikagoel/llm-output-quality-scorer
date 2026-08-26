"""Thin client for a local Ollama server — zero-cost, no API key, no billing.

Tradeoff (see README): using a local open-weight model (llama3.2, ~3B) instead of a paid
hosted API keeps this project genuinely free to run and reproduce, at the cost of judge/draft
quality relative to a frontier model. The calibration step exists specifically to check whether
that quality tradeoff is acceptable for this task — see the calibration report before trusting
the scorer's output.
"""
import json

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"


def chat(model: str, prompt: str, json_mode: bool = False, temperature: float = 0.7) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": temperature},
    }
    if json_mode:
        payload["format"] = "json"

    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def chat_json(model: str, prompt: str, temperature: float = 0.0, retries: int = 2) -> dict:
    last_err = None
    for attempt in range(retries + 1):
        raw = chat(model, prompt, json_mode=True, temperature=temperature)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            last_err = e
            prompt = prompt + f"\n\nYour previous response was not valid JSON ({e}). Return ONLY valid JSON, nothing else."
    raise RuntimeError(f"Model never returned valid JSON after {retries + 1} attempts: {last_err}")
