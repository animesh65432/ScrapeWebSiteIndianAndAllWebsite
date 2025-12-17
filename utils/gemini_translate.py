from service.Gemini import model
import asyncio

sem = asyncio.Semaphore(3)  

async def gemini_translate(prompt: str, retries: int = 3) -> str:
    async with sem:
        for attempt in range(retries):
            try:
                response = await model.generate_content_async(prompt)
                return response.text.strip()
            except Exception as e:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
