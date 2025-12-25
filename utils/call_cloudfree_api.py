import httpx
from config import config
import asyncio

async def call_cloudflare(
    prompt: str,
    model: str = "@cf/meta/llama-3.1-70b-instruct",
    retries: int = 3,
    delay: int = 3
) -> str:
    
    accounts = [
        {
            "id": config["CLOUDFARE_MODEL_ACCOUNT_ID"],
            "token": config["CLOUDFARE_MODEL_API_TOKEN"]
        },
        {
            "id": config["SECOND_CLOUDFARE_MODEL_ACCOUNT_ID"],
            "token": config["SECOND_CLOUDFARE_MODEL_API_TOKEN"]
        }
    ]

   
    for idx, account in enumerate(accounts):
        if not account['token'] or len(account['token']) < 20:
            print(f"⚠️  Account {idx + 1} has invalid token format")
    
    async with httpx.AsyncClient() as client:
        for account_idx, account in enumerate(accounts, 1):
            url = f"https://api.cloudflare.com/client/v4/accounts/{account['id']}/ai/run/{model}"
            
            headers = {
                "Authorization": f"Bearer {account['token']}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            for attempt in range(1, retries + 1):
                try:
                    response = await client.post(url, headers=headers, json=payload, timeout=120.0)
                    
                    # Handle 401 Unauthorized
                    if response.status_code == 401:
                        print(f"❌ Account {account_idx} authentication failed (401)")
                        print(f"   Token preview: {account['token'][:10]}...")
                        print(f"   Check your API token for account {account['id']}")
                        break  # Don't retry auth failures, move to next account
                    
                    # Handle rate limiting
                    if response.status_code == 429:
                        print(f"⏸️  Account {account_idx} rate limited (429)")
                        break  # Try next account
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    # Check for API errors in response body
                    if not result.get('success', True):
                        errors = result.get('errors', [])
                        error_codes = [e.get('code') for e in errors]
                        
                        # Cloudflare quota/rate limit error codes
                        if any(code in [10000, 10001, 10002] for code in error_codes):
                            print(f"⏸️  Account {account_idx} quota exceeded: {errors}")
                            break  # Try next account
                        else:
                            raise ValueError(f"API error: {errors}")
                    
                    # Validate response
                    if not result.get('result') or not result['result'].get('response'):
                        raise ValueError("Empty response from API")
                    
                    print(f"✅ Account {account_idx} succeeded")
                    return result['result']['response'].strip()
                    
                except httpx.HTTPStatusError as e:
                    status = e.response.status_code
                    
                    if status == 401:
                        print(f"❌ Account {account_idx} - Invalid API token")
                        break
                    elif status == 429:
                        print(f"⏸️  Account {account_idx} - Rate limited")
                        break
                    else:
                        print(f"⚠️  Account {account_idx}, Attempt {attempt}/{retries}: HTTP {status}")
                        
                        if attempt < retries:
                            wait_time = delay * attempt
                            print(f"   Retrying in {wait_time}s...")
                            await asyncio.sleep(wait_time)
                        else:
                            print(f"❌ Account {account_idx} - All retries exhausted")
                            break
                        
                except Exception as e:
                    error_msg = str(e)
                    print(f"⚠️  Account {account_idx}, Attempt {attempt}/{retries}: {error_msg}")
                    
                    if attempt < retries:
                        wait_time = delay * attempt
                        print(f"   Retrying in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        print(f"❌ Account {account_idx} - All retries exhausted")
                        break
        
       
        raise Exception(
            f"❌ All {len(accounts)} accounts failed.\n"
            f"   Check your API tokens at: https://dash.cloudflare.com/profile/api-tokens"
        )

