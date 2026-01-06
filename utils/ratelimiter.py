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
