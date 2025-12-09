import httpx
import asyncio
from config.headers import headers
from utils.makeurlwithscaperdo import makeurlwithscaperdo


async def fetch_with_httpx(url: str, part:str,timeout: int = 30, retries: int = 3) -> str:

    url = makeurlwithscaperdo(url,part=part,isScraperAPIUsed=True)

    for attempt in range(1, retries + 1):
        try:
            print(f"[httpx Attempt {attempt}/{retries}] Fetching {url}...")
            
            async with httpx.AsyncClient(
                timeout=timeout,
                follow_redirects=True,
                headers=headers,
                verify=False , # Ignore SSL errors
            ) as client:
                response = await client.get(url)
                
                if response.status_code == 200:
                    print(f"✅ httpx success! ({len(response.text)} bytes)")
                    return response.text
                else:
                    print(f"❌ httpx got status {response.status_code}")
                    
        except httpx.TimeoutException:
            print(f"[httpx Attempt {attempt}/{retries}] ⏱️  Timeout")
        except httpx.ConnectError as e:
            print(f"[httpx Attempt {attempt}/{retries}] 🔌 Connection error: {e}")
        except Exception as e:
            print(f"[httpx Attempt {attempt}/{retries}] ❌ Error: {e}")
        
        if attempt < retries:
            await asyncio.sleep(2 * attempt)
    
    print("❌ httpx failed all retries")
    return None
