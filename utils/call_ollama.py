import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"

async def call_ollama(
    prompt: str,
    target_language: str,
    client: httpx.AsyncClient
) -> str:

    system_context = (
        "You are a professional translator for Indian government announcements. "
        f"Translate ONLY to {target_language} script. Do not mix scripts."
    )

    payload = {
        "model": MODEL,
        "prompt": f"{system_context}\n\n{prompt}",
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 800,
        }
    }

    response = await client.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    translated = response.json().get("response", "").strip()
    if not translated:
        raise Exception("Empty response from Ollama")

    return translated
