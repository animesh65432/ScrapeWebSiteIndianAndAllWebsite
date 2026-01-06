from service.Groq import Groqclient
from app_types.govt_item import GovtItem
from prompts.classifyAi import get_prompt
import asyncio

class RateLimiter:
    """
    Token bucket rate limiter for API calls.
    Limits both concurrent requests and tokens per minute.
    """
    def __init__(self, max_concurrent: int = 3, tokens_per_minute: int = 7000):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.tokens_per_minute = tokens_per_minute
        self.tokens_used = 0
        self.window_start = None
    
    async def acquire(self, estimated_tokens: int = 1200):
        """Acquire permission to make an API call."""
        async with self.semaphore:
            now = asyncio.get_event_loop().time()
            
            # Reset window if 60 seconds have passed
            if self.window_start is None or (now - self.window_start) >= 60:
                self.window_start = now
                self.tokens_used = 0
            
            # Wait if we would exceed token limit
            if self.tokens_used + estimated_tokens > self.tokens_per_minute:
                wait_time = 60 - (now - self.window_start) + 1
                print(f"⏳ Token limit reached, waiting {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)
                self.window_start = asyncio.get_event_loop().time()
                self.tokens_used = 0
            
            self.tokens_used += estimated_tokens
            return True



rate_limiter = RateLimiter(max_concurrent=3, tokens_per_minute=7000)


async def classify_ai(item: GovtItem) -> str:
    
    if not isinstance(item, dict):
        return "skip"
    
    # Estimate tokens (rough approximation)
    prompt = get_prompt(item)
    
    estimated_tokens = len(prompt.split()) * 1.3  # Rough token estimate
    
    # Wait for rate limiter permission
    await rate_limiter.acquire(estimated_tokens)
    
    try:
        response = await Groqclient.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0
        )
        
        result = response.choices[0].message.content.strip().lower()
        result = "important" if "important" in result else "skip"
        
        print(f"✓ {result.upper()}: {item.get('title', '')[:60]}")
        return result
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:100]}")
        return "skip"