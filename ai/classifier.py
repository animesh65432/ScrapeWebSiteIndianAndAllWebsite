from service.Groq import Groqclient
from app_types.govt_item import GovtItem
from prompts.classifyAi import get_prompt
import asyncio

class RateLimiter:
    def __init__(self, max_concurrent=3, tokens_per_minute=7000):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.tokens_per_minute = tokens_per_minute
        self.tokens_used = 0
        self.window_start = asyncio.get_event_loop().time()
        self.lock = asyncio.Lock()

    async def wait_for_tokens(self, estimated_tokens):
        async with self.lock:
            now = asyncio.get_event_loop().time()
            elapsed = now - self.window_start

            if elapsed >= 60:
                self.window_start = now
                self.tokens_used = 0

            if self.tokens_used + estimated_tokens > self.tokens_per_minute:
                wait_time = 60 - elapsed + 1
                print(f"⏳ Token limit reached, waiting {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)
                self.window_start = asyncio.get_event_loop().time()
                self.tokens_used = 0

            self.tokens_used += estimated_tokens
            
rate_limiter = RateLimiter(max_concurrent=3, tokens_per_minute=7000)

async def classify_ai(item: GovtItem) -> str:
    if not isinstance(item, dict):
        return "skip"

    prompt = get_prompt(item)
    estimated_tokens = int(len(prompt.split()) * 1.3)

    for attempt in range(3):
        try:
            async with rate_limiter.semaphore:
                await rate_limiter.wait_for_tokens(estimated_tokens)

                response = await Groqclient.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": "Reply with only: important or skip"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=5,
                    temperature=0
                )

            result = response.choices[0].message.content.strip().lower()
            result = "important" if "important" in result else "skip"

            print(f"✓ {result.upper()}: {item.get('title','')[:60]}")
            return result

        except Exception as e:
            if "429" in str(e):
                wait = 2 ** attempt
                print(f"⚠️ 429 received, retrying in {wait}s...")
                await asyncio.sleep(wait)
            else:
                print(f"❌ ERROR: {str(e)[:100]}")
                return "skip"

    print("❌ Failed after retries")
    return "skip"
