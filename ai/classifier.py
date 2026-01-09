from service.Groq import Groqclient
from app_types.govt_item import GovtItem
from prompts.classifyAi import get_prompt
import asyncio

async def classify_ai(
    item: GovtItem,
    max_retries: int = 3,
    retry_delay: float = 2.0
) -> str:
    
    # Validate input
    if not isinstance(item, dict):
        print(f"   ⚠️  WARNING: classify_ai received {type(item).__name__}")
        return "news"
    
    # Get prompt
    prompt = get_prompt(item)
    
    # Retry loop
    for attempt in range(max_retries):
        try:
            # Add small delay to respect rate limits
            if attempt > 0:
                delay = retry_delay * (2 ** (attempt - 1))  # Exponential backoff
                print(f"   🔄 Retry {attempt + 1}/{max_retries} after {delay}s: {item.get('title', '')[:30]}")
                await asyncio.sleep(delay)
            
            # Make API call with asyncio.to_thread for sync client
            response = await asyncio.to_thread(
                Groqclient.chat.completions.create,
                model="gemma2-9b-it",
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
                max_tokens=5,
                temperature=0,
                timeout=10  # 10 second timeout
            )
            
            result = response.choices[0].message.content.strip().lower()
            
            # Validate result
            if "announcement" in result:
                result = "announcement"
            elif "news" in result:
                result = "news"
            elif result not in ["news", "announcement"]:
                print(f"   ⚠️  Unexpected response '{result}', defaulting to 'announcement'")
                result = "announcement"
            
            # Success - return result
            return result
            
        except asyncio.TimeoutError:
            print(f"   ⏱️  Timeout on attempt {attempt + 1}: {item.get('title', '')[:30]}")
            if attempt == max_retries - 1:
                print(f"   ❌ Max retries reached, classifying as 'news'")
                return "news"
                
        except Exception as e:
            error_msg = str(e).lower()
            
            # Handle rate limit errors
            if "rate_limit" in error_msg or "429" in error_msg:
                print(f"   🚦 Rate limit hit on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * 2)  # Wait longer for rate limits
                    continue
                else:
                    return "news"
            
            # Handle other errors
            print(f"   ❌ Error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                print(f"   ❌ Max retries reached, classifying as 'news'")
                return "news"
    
    # Fallback (should never reach here)
    return "news"
    