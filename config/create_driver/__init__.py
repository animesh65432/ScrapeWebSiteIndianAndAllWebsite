from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options
import asyncio
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from utils.cleanup_chrome_processes import cleanup_chrome_processes

async def create_driver(retries=3, delay=3):
    """Create Chrome driver with retry logic - runs in executor to avoid blocking"""
    
    def _create_driver_sync():
        """Synchronous driver creation (runs in thread pool)"""
        chrome_options = Get_Chrome_Options()
        chrome_options.page_load_strategy = "normal"
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(40)
            driver.implicitly_wait(20)
            return driver
        except Exception as e:
            print(f"[create_driver_sync] Error: {e}")
            return None
    
    for attempt in range(1, retries + 1):
        try:
            # Run driver creation in thread pool
            loop = asyncio.get_event_loop()
            driver = await loop.run_in_executor(None, _create_driver_sync)
            
            if driver:
                return driver
            
            print(f"[Driver Retry {attempt}/{retries}] Failed to create driver")
            
        except WebDriverException as e:
            error_msg = str(e)
            print(f"[Driver Retry {attempt}/{retries}] WebDriver error: {error_msg[:150]}")
            
            # Cleanup on renderer connection errors
            if "unable to connect to renderer" in error_msg:
                print(f"[Driver Retry {attempt}/{retries}] Cleaning up zombie processes...")
                await cleanup_chrome_processes()
        
        except Exception as e:
            print(f"[Driver Retry {attempt}/{retries}] Unexpected error: {e}")
        
        if attempt < retries:
            await asyncio.sleep(delay)
    
    print("[create_driver] ❌ All retries exhausted")
    return None