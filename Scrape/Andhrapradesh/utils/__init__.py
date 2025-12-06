import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit

async def scrape_website(url: str, days_back: int = 1):
    """
    Fixed version with proper async handling for form interactions
    """
    driver = None
    try:
        driver = await create_driver()
        if not driver:
            print(f"[scrape_website] Failed to create driver for {url}")
            return []
        
        # Load page with retry
        if not await load_with_retry(driver ,url,html_element="#results-table" ,retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        # Calculate date range
        current_date = datetime.now()
        to_date_obj = current_date - timedelta(days=1)  # Yesterday
        from_date_obj = current_date - timedelta(days=days_back)  # X days back
        
        from_date = from_date_obj.strftime("%d-%m-%Y")
        to_date = to_date_obj.strftime("%d-%m-%Y")
        
        # All Selenium interactions wrapped in executor
        loop = asyncio.get_event_loop()
        
        def interact_with_form():
            """
            Synchronous function containing all blocking Selenium operations
            """
            wait = WebDriverWait(driver, 10)
            
            # Fill in the date fields
            from_date_input = wait.until(
                EC.presence_of_element_located((By.ID, "txtfrmdate"))
            )
            to_date_input = driver.find_element(By.ID, "txttodate")
            
            # Clear and enter dates
            from_date_input.clear()
            from_date_input.send_keys(from_date)
            
            to_date_input.clear()
            to_date_input.send_keys(to_date)
            
            # Click search button
            search_button = driver.find_element(By.ID, "BtnSearch")
            search_button.click()
            
            # Wait for results to load
            # Better: wait for specific element instead of sleep
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "table"))
                )
            except:
                pass  # Continue even if table doesn't appear
            
            return driver.page_source
        
        # Run all form interactions in executor to avoid blocking
        try:
            html = await loop.run_in_executor(None, interact_with_form)
        except Exception as e:
            print(f"Error during form interaction: {e}")
            await safe_quit(driver=driver)
            return []
        
        # Close driver before parsing
        await safe_quit(driver=driver)
        driver = None
        
        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract announcements
        announcements = extract_announcements(soup)
        
        return announcements if announcements else []
    
    except Exception as e:
        print(f"Andhra Pradesh scrape_website error: {e}")
        import traceback
        traceback.print_exc()
        return []
    
    finally:
        if driver:
            await safe_quit(driver=driver)


def extract_announcements(soup):
    """
    Extract announcements from BeautifulSoup object
    Pure parsing - no Selenium, so doesn't need to be async
    """
    announcements = []
    
    try:
        # Add your parsing logic here
        # Example:
        table = soup.find('table', {'id': 'results-table'})  # Adjust selector
        if not table:
            return []
        
        rows = table.find_all('tr')[1:]  # Skip header
        
        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) >= 3:  # Adjust based on table structure
                    announcements.append({
                        'title': cells[0].text.strip(),
                        'date': cells[1].text.strip(),
                        'link': cells[2].find('a')['href'] if cells[2].find('a') else '',
                        'state': 'AndhraPradesh'
                    })
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
        
    except Exception as e:
        print(f"Error in extract_announcements: {e}")
    
    return announcements
