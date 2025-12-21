import httpx
from config import config
import asyncio

async def call_cloudflare(
    prompt: str,
    max_tokens: int = 512,
    model: str = "@cf/google/gemma-3-12b-it",
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
    
    async with httpx.AsyncClient() as client:
        for account_idx, account in enumerate(accounts):
            url = f"https://api.cloudflare.com/client/v4/accounts/{account['id']}/ai/run/{model}"
            
            headers = {
                "Authorization": f"Bearer {account['token']}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens
            }
            
            for attempt in range(retries):
                try:
                    response = await client.post(url, headers=headers, json=payload, timeout=30.0)
                    
                    # Check if it's a quota error (status 429 or specific error codes)
                    if response.status_code == 429:
                        print(f"Account {account_idx + 1} quota exceeded")
                        break  # Try next account
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    # Check for quota errors in response body
                    if not result.get('success', True):
                        errors = result.get('errors', [])
                        for error in errors:
                            # Cloudflare quota error codes
                            if error.get('code') in [10000, 10001]:  # Adjust based on actual error codes
                                print(f"Account {account_idx + 1} quota exceeded: {error}")
                                break
                        else:
                            raise ValueError(f"API error: {errors}")
                        break  # Try next account
                    
                    if not result.get('result') or not result['result'].get('response'):
                        raise ValueError("Empty response from API")
                    
                    return result['result']['response'].strip()
                    
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 429:
                        print(f"Account {account_idx + 1} rate limited")
                        break  # Try next account
                    print(f"Account {account_idx + 1}, Attempt {attempt + 1} failed: {str(e)}")
                    
                    if attempt < retries - 1:
                        await asyncio.sleep(delay * (attempt + 1))
                    else:
                        print(f"All retries exhausted for account {account_idx + 1}")
                        break  # Try next account
                        
                except Exception as e:
                    print(f"Account {account_idx + 1}, Attempt {attempt + 1} failed: {str(e)}")
                    
                    if attempt < retries - 1:
                        await asyncio.sleep(delay * (attempt + 1))
                    else:
                        print(f"All retries exhausted for account {account_idx + 1}")
                        break  # Try next account
        
        # If we get here, all accounts failed
        raise Exception(f"All {len(accounts)} accounts failed after {retries} retries each")