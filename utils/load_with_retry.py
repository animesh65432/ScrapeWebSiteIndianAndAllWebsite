import asyncio
from typing import Optional
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException

async def load_with_retry(
    driver: Optional[webdriver.Chrome], 
    url: str, 
    retries: int = 3, 
    delay: int = 3,
    timeout: int = 60  # Increased default timeout
) -> bool:
    """
    Async retry logic for loading pages with Selenium.
    Enhanced with better timeout handling and recovery.
    """
    if driver is None:
        print(f"[load_with_retry] ❌ Driver is None, cannot load {url}")
        return False
    
    for attempt in range(1, retries + 1):
        try:
            # Temporarily increase page load timeout for slow sites
            loop = asyncio.get_event_loop()
            
            def load_page():
                """Load page with custom timeout"""
                driver.set_page_load_timeout(timeout)
                driver.get(url)
                return driver.page_source
            
            # Run with timeout protection
            try:
                page_source = await asyncio.wait_for(
                    loop.run_in_executor(None, load_page),
                    timeout=timeout + 5  # Give extra buffer
                )
            except asyncio.TimeoutError:
                print(f"[Retry {attempt}/{retries}] Asyncio timeout for {url}")
                continue
            
            # Validate content
            if page_source and len(page_source) > 100:
                return True
            else:
                print(f"[Retry {attempt}/{retries}] Page loaded but content is empty/too short")
                
        except TimeoutException as e:
            print(f"[Retry {attempt}/{retries}] Selenium timeout for {url}: {str(e)[:100]}")
            
            # On timeout, try to stop page load and continue
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, driver.execute_script, "window.stop();")
                
                # Check if we got partial content
                page_source = await loop.run_in_executor(None, lambda: driver.page_source)
                if page_source and len(page_source) > 1000:  # If we got substantial content
                    print(f"[Retry {attempt}/{retries}] Using partial content from timeout")
                    return True
            except:
                pass
            
        except WebDriverException as e:
            error_msg = str(e)
            
            # Check for session issues
            if "invalid session id" in error_msg.lower():
                print(f"[Retry {attempt}/{retries}] Session lost for {url}, driver needs restart")
                return False  # Signal that driver needs to be recreated
            
            # Check for renderer issues
            if "renderer" in error_msg.lower() or "disconnected" in error_msg.lower():
                print(f"[Retry {attempt}/{retries}] Renderer issue for {url}, may need driver restart")
                if attempt == retries:  # Last attempt
                    return False
            
            print(f"[Retry {attempt}/{retries}] Failed to load {url}: {error_msg[:200]}")
            
        except Exception as e:
            print(f"[Retry {attempt}/{retries}] Unexpected error loading {url}: {e}")
        
        if attempt < retries:
            # Exponential backoff for retries
            wait_time = delay * (1.5 ** (attempt - 1))
            await asyncio.sleep(min(wait_time, 10))  # Cap at 10 seconds
    
    return False
