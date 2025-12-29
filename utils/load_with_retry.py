import asyncio
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

async def load_with_retry(
    driver,
    url: str,
    html_element: str,
    part: str = "",
    retries: int = 3,
    delay: int = 3,
    timeout: int = 30
) -> bool:

    if driver is None:
        print("❌ Driver is None")
        return False

    if not url:
        print("❌ URL is empty")
        return False

    # Detect CI environment and adjust parameters
    is_ci = os.getenv('GITHUB_ACTIONS') == 'true'
    
    print(f"🔄 Loading URL for part: {part}")
    
    if is_ci:
        timeout = max(timeout, 60)  # Minimum 60s timeout in CI
        delay = max(delay, 5)  # Longer delay between retries
        retries = max(retries, 4)  # More retries in CI

    loop = asyncio.get_event_loop()

    for attempt in range(1, retries + 1):
        try:
            print(f"[Retry {attempt}/{retries}] Loading {url}...")
            
            await loop.run_in_executor(None, lambda: url)
            
            # Small delay to let page start loading
            await asyncio.sleep(2)

            # Wait for the required HTML element
            await loop.run_in_executor(
                None,
                lambda: WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, html_element))
                ),
            )

            print(f"✅ Page loaded successfully and element found: {html_element}")
            return True

        except TimeoutException as e:
            print(f"[Retry {attempt}/{retries}] ❌ Timeout waiting for element: {html_element}")
            
            # Try to get page title for debugging
            try:
                title = driver.title
                print(f"   📄 Page title: {title}")
            except:
                pass
            
            if attempt == retries:
                print("❌ Max retries reached — giving up")
                print(f"❌ Page failed to load after {retries} retries")
                return False

            wait_time = delay * attempt  # Progressive delay
            print(f"⏳ Waiting {wait_time}s before retry...")
            await asyncio.sleep(wait_time)
            
        except WebDriverException as e:
            error_msg = str(e)
            print(f"[Retry {attempt}/{retries}] ❌ WebDriver error: {error_msg[:200]}")
            
            # Check for DNS errors
            if "ERR_NAME_NOT_RESOLVED" in error_msg:
                print(f"   ⚠️  DNS resolution failed - site may be down or geo-restricted")
                if is_ci:
                    print(f"   ℹ️  This site is known to be unreliable in GitHub Actions")
                    return False  # Don't retry DNS errors in CI
            
            if attempt == retries:
                print("❌ Max retries reached — giving up")
                print(f"❌ Page failed to load after {retries} retries")
                return False

            wait_time = delay * attempt
            print(f"⏳ Waiting {wait_time}s before retry...")
            await asyncio.sleep(wait_time)
            
        except Exception as e:
            print(f"[Retry {attempt}/{retries}] ❌ Unexpected error: {type(e).__name__}: {str(e)[:200]}")
            
            if attempt == retries:
                print("❌ Max retries reached — giving up")
                return False
            
            wait_time = delay * attempt
            print(f"⏳ Waiting {wait_time}s before retry...")
            await asyncio.sleep(wait_time)

    return False