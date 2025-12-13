import httpx
import asyncio
from config.headers import headers
import gzip
import brotli

async def fetch_with_httpx(
    url: str, 
    timeout: int = 30, 
    retries: int = 3,
    return_status: bool = False
) -> str | tuple[str, int] | None:
    
    for attempt in range(1, retries + 1):
        try:
            # Create headers that explicitly handle compression
            fetch_headers = {
                **headers,
                'Accept-Encoding': 'gzip, deflate, br',  # Accept compressed content
            }
            
            async with httpx.AsyncClient(
                timeout=timeout,
                follow_redirects=True, 
                headers=fetch_headers,
                verify=False  # Change to True in production
            ) as client:
                
                response = await client.get(url)
                
                # Debug: Check content encoding
                response.headers.get('content-encoding', 'none')
               
                
                if response.status_code == 200:
                    # httpx automatically decompresses, but let's verify
                    html = response.text
                    
                    # Check if we got valid HTML
                    if html.startswith('<!DOCTYPE') or html.startswith('<html'):
                        print(f"✅ httpx success! ({len(html)} bytes)")
                        if return_status:
                            return html, response.status_code
                        return html
                    else:
                        
                        # Try manual decoding if needed
                        try:
                            
                            raw_content = response.content
                            
                            # Try gzip
                            try:
                                html = gzip.decompress(raw_content).decode('utf-8')
                            except:
                                pass
                            
                            # Try brotli
                            if not (html.startswith('<!DOCTYPE') or html.startswith('<html')):
                                try:
                                    html = brotli.decompress(raw_content).decode('utf-8')
                                except:
                                    pass
                            
                            if html.startswith('<!DOCTYPE') or html.startswith('<html'):
                                if return_status:
                                    return html, response.status_code
                                return html
                        except Exception as e:
                            print(f"❌ Manual decompression failed: {e}")
                        
                        print("❌ Could not decode response as HTML")
                        if return_status:
                            return None, response.status_code
                        return None
                        
                elif 400 <= response.status_code < 500:
                    # Client error - don't retry
                    print(f"❌ httpx got client error {response.status_code} - not retrying")
                    if return_status:
                        return None, response.status_code
                    return None
                else:
                    print(f"❌ httpx got status {response.status_code}")
                    
        except httpx.TimeoutException:
            print(f"[httpx Attempt {attempt}/{retries}] ⏱️  Timeout")
        except httpx.ConnectError as e:
            print(f"[httpx Attempt {attempt}/{retries}] 🔌 Connection error: {e}")
        except Exception as e:
            print(f"[httpx Attempt {attempt}/{retries}] ❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        if attempt < retries:
            await asyncio.sleep(2 * attempt)
    
    print("❌ httpx failed all retries")
    return None