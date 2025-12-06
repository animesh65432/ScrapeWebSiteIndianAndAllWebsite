import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


async def load_with_retry(
    driver,
    url: str,
    html_element: str,
    retries: int = 3,
    delay: int = 3,
    timeout: int = 30,
) -> bool:
    """
    Load a page and wait until a specific HTML element appears.
    Retries the entire process on failure.
    """

    if driver is None:
        print("❌ Driver is None")
        return False

    if not url:
        print("❌ URL is empty")
        return False

    loop = asyncio.get_event_loop()

    for attempt in range(1, retries + 1):
        try:
            # Run driver.get() in executor (non-blocking for event loop)
            await loop.run_in_executor(None, lambda: driver.get(url))

            # Wait for the required HTML element
            await loop.run_in_executor(
                None,
                lambda: WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, html_element))
                ),
            )

            print(f"✅ Page loaded successfully and element found: {html_element}")
            return True

        except (TimeoutException, WebDriverException) as e:
            print(f"[Retry {attempt}/{retries}] ❌ Failed to load {url}: {e}")

            if attempt == retries:
                print("❌ Max retries reached — giving up")
                return False

            await asyncio.sleep(delay)

    return False
