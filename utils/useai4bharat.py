import httpx
import asyncio
from config import config

MAX_RETRIES = 10
INITIAL_BACKOFF = 2  # seconds


async def translate_using_ai4bharat(text: str, target_lang: str) -> str:
    payload = {
        "sourceLanguage": "en",
        "targetLanguage": target_lang,
        "input": text,
        "task": "translation",
        "serviceId": "ai4bharat/indictrans--gpu-t4",
        "track": True
    }

    backoff = INITIAL_BACKOFF

    async with httpx.AsyncClient(timeout=60) as client:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = await client.post(
                    config["AIBHARAT_URL"],
                    json=payload
                )
                resp.raise_for_status()

                data = resp.json()
                return data["output"][0]["target"]

            except httpx.HTTPStatusError as e:
                print(
                    f"⚠️ HTTP error ({resp.status_code}) "
                    f"for {target_lang}, attempt {attempt} , error: {e}"
                )

            except httpx.RequestError as e:
                print(
                    f"⚠️ Network error for {target_lang}, attempt {attempt}: {e}"
                )

            if attempt < MAX_RETRIES:
                print(f"🔁 Retrying in {backoff}s...")
                await asyncio.sleep(backoff)
                backoff *= 2 

        raise Exception(f"Translation failed after {MAX_RETRIES} retries")
