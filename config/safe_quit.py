import asyncio
from selenium import webdriver

async def safe_quit(driver: webdriver.Chrome = None):
    """Safely quit driver without blocking event loop"""
    if not driver:
        return
    
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, driver.quit)
    except Exception as e:
        print(f"[safe_quit] Error during quit (non-critical): {e}")
        # Force kill if quit fails
        try:
            await loop.run_in_executor(None, driver.service.stop)
        except:
            pass