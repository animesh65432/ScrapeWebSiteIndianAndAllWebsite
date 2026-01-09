from service.Groq import Groqclient
from app_types.govt_item import GovtItem
from prompts.classifyAi import get_prompt
import asyncio

async def classify_ai(
    item: GovtItem,
    max_retries: int = 10,
    retry_delay: float = 2.0
) -> str:

    if not isinstance(item, dict):
        return "news"

    prompt = get_prompt(item)

    for attempt in range(max_retries):
        try:
            if attempt > 0:
                delay = retry_delay * (2 ** (attempt - 1))
                print(f"🔄 Retry {attempt + 1}/{max_retries} after {delay}s: {item.get('title','')[:30]}")
                await asyncio.sleep(delay)

            response = await Groqclient.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": "Classify as 'announcement' (govt issued) or 'news' (media). Reply with one word only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                timeout=10
            )

            print(response)

            result = response.choices[0].message.content.strip().lower()

            if "announcement" in result:
                return "announcement"
            if "news" in result:
                return "news"

            print(f"⚠️ Unexpected response '{result}', defaulting to 'announcement'")
            return "announcement"

        except asyncio.TimeoutError:
            print(f"⏱️ Timeout on attempt {attempt + 1}")
            if attempt == max_retries - 1:
                return "news"

        except Exception as e:
            msg = str(e).lower()
            if "rate" in msg or "429" in msg:
                await asyncio.sleep(retry_delay * 2)
                continue

            print(f"❌ Error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                return "news"

    return "news"

