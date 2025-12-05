import asyncio
from typing import Optional
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

async def load_with_retry(
    driver: Optional[webdriver.Chrome], 
    url: str, 
    retries: int = 3, 
    delay: int = 3
) -> bool:
    """
    Async retry logic for loading pages with Selenium.
    Runs blocking Selenium calls in thread pool to avoid blocking event loop.
    """
    if driver is None:
        print(f"[load_with_retry] ❌ Driver is None, cannot load {url}")
        return False
    
    for attempt in range(1, retries + 1):
        try:
            # Run blocking Selenium call in executor
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, driver.get, url)
            
            # Brief wait for page to start loading
            await asyncio.sleep(0.5)
            
            # Check if we got content (also run in executor)
            page_source = await loop.run_in_executor(None, lambda: driver.page_source)
            
            if page_source and len(page_source) > 100:
                return True
            else:
                print(f"[Retry {attempt}/{retries}] Page loaded but content is empty/too short")
                
        except WebDriverException as e:
            error_msg = str(e)
            
            # Check for session issues
            if "invalid session id" in error_msg.lower():
                print(f"[Retry {attempt}/{retries}] Session lost for {url}, driver needs restart")
                return False  # Signal that driver needs to be recreated
            
            print(f"[Retry {attempt}/{retries}] Failed to load {url}: {error_msg[:200]}")
            
        except Exception as e:
            print(f"[Retry {attempt}/{retries}] Unexpected error loading {url}: {e}")
        
        if attempt < retries:
            await asyncio.sleep(delay)  # FIXED: Use asyncio.sleep
    
    return False