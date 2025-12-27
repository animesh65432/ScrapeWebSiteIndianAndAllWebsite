import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import time

async def scrape_website(url: str, days_back: int = 1):
    """
    Fixed version with robust async handling for form interactions
    """
    driver = None
    try:
        driver = await create_driver()
        if not driver:
            print(f"[scrape_website] Failed to create driver for {url}")
            return []
        
        # Load page with retry
        if not await load_with_retry(driver, url, html_element="div", part="south_india", retries=3, delay=3,dont_use_proxy=True):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        # Calculate date range
        current_date = datetime.now()
        to_date_obj = current_date - timedelta(days=1)  # Yesterday
        from_date_obj = current_date - timedelta(days=days_back)  # X days back
        
        from_date = from_date_obj.strftime("%d-%m-%Y")
        to_date = to_date_obj.strftime("%d-%m-%Y")
        
        print(f"🔍 Searching from {from_date} to {to_date}")
        
        # All Selenium interactions wrapped in executor
        loop = asyncio.get_event_loop()
        
        def interact_with_form():
            """
            Synchronous function with robust Selenium operations
            """
            try:
                wait = WebDriverWait(driver, 15)
                
                # Check for iframes first
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                if iframes:
                    print(f"Found {len(iframes)} iframes, switching to first one")
                    driver.switch_to.frame(0)
                    wait = WebDriverWait(driver, 15)  # Reinitialize wait after frame switch
                
                # Wait for page to be fully loaded
                time.sleep(2)
                
                # Method 1: Try standard interaction
                try:
                    # Fill from date
                    from_date_input = wait.until(
                        EC.presence_of_element_located((By.ID, "txtfrmdate"))
                    )
                    
                    # Scroll into view
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", from_date_input)
                    time.sleep(0.5)
                    
                    # Clear using multiple methods
                    from_date_input.click()
                    from_date_input.clear()
                    driver.execute_script("arguments[0].value = '';", from_date_input)
                    time.sleep(0.3)
                    
                    # Enter date
                    from_date_input.send_keys(from_date)
                    print(f"✓ From date set: {from_date}")
                    
                    # Fill to date
                    to_date_input = driver.find_element(By.ID, "txttodate")
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", to_date_input)
                    time.sleep(0.3)
                    
                    to_date_input.click()
                    to_date_input.clear()
                    driver.execute_script("arguments[0].value = '';", to_date_input)
                    time.sleep(0.3)
                    
                    to_date_input.send_keys(to_date)
                    print(f"✓ To date set: {to_date}")
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"Standard interaction failed: {e}")
                    # Method 2: Try JavaScript injection
                    print("Trying JavaScript method...")
                    driver.execute_script(f"""
                        document.getElementById('txtfrmdate').value = '{from_date}';
                        document.getElementById('txttodate').value = '{to_date}';
                    """)
                    time.sleep(0.5)
                
                # Click search button with multiple fallback methods
                search_clicked = False
                
                # Method 1: Standard click
                try:
                    search_button = wait.until(
                        EC.element_to_be_clickable((By.ID, "BtnSearch"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", search_button)
                    time.sleep(0.5)
                    search_button.click()
                    search_clicked = True
                    print("✓ Search button clicked (standard)")
                except (ElementClickInterceptedException, TimeoutException) as e:
                    print(f"Standard click failed: {e}")
                
                # Method 2: JavaScript click
                if not search_clicked:
                    try:
                        search_button = driver.find_element(By.ID, "BtnSearch")
                        driver.execute_script("arguments[0].click();", search_button)
                        search_clicked = True
                        print("✓ Search button clicked (JavaScript)")
                    except Exception as e:
                        print(f"JavaScript click failed: {e}")
                
                # Method 3: Submit form directly
                if not search_clicked:
                    try:
                        form = driver.find_element(By.TAG_NAME, "form")
                        driver.execute_script("arguments[0].submit();", form)
                        search_clicked = True
                        print("✓ Form submitted directly")
                    except Exception as e:
                        print(f"Form submit failed: {e}")
                        raise Exception("All click methods failed")
                
                # Wait for results with multiple strategies
                print("⏳ Waiting for results...")
                
                result_loaded = False
                
                # Try waiting for table
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.TAG_NAME, "table"))
                    )
                    result_loaded = True
                    print("✓ Results table loaded")
                except TimeoutException:
                    print("Table wait timeout")
                
                # Try waiting for any common result container
                if not result_loaded:
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "results"))
                        )
                        result_loaded = True
                        print("✓ Results container loaded")
                    except:
                        pass
                
                # Fallback: just wait a bit
                if not result_loaded:
                    print("Using fallback wait...")
                    time.sleep(5)
                
                # Get page source
                html = driver.page_source
                
                # Switch back from iframe if we switched
                if iframes:
                    driver.switch_to.default_content()
                
                return html
                
            except Exception as e:
                print(f"❌ Error in interact_with_form: {e}")
                import traceback
                traceback.print_exc()
                
                # Try to get page source anyway
                try:
                    return driver.page_source
                except:
                    raise e
        
        # Run all form interactions in executor
        try:
            html = await loop.run_in_executor(None, interact_with_form)
        except Exception as e:
            print(f"❌ Error during form interaction: {e}")
            await safe_quit(driver=driver)
            return []
        
        # Close driver before parsing
        await safe_quit(driver=driver)
        driver = None
        
        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract announcements
        announcements = extract_announcements(soup)
        
        print(f"✅ Found {len(announcements)} announcements")
        return announcements if announcements else []
    
    except Exception as e:
        print(f"❌ Andhra Pradesh scrape_website error: {e}")
        import traceback
        traceback.print_exc()
        return []
    
    finally:
        if driver:
            await safe_quit(driver=driver)


def extract_announcements(soup):
    """
    Extract announcements from BeautifulSoup object
    """
    announcements = []
    
    try:
        # Try multiple table selectors
        table = (
            soup.find('table', {'id': 'GridView1'}) or  # Common ID for AP govt sites
            soup.find('table', {'class': 'results'}) or
            soup.find('table', {'id': 'results-table'}) or
            soup.find('table')  # Any table as fallback
        )
        
        if not table:
            print("⚠️ No table found in results")
            # Debug: print available tables
            all_tables = soup.find_all('table')
            print(f"Total tables found: {len(all_tables)}")
            return []
        
        print(f"✓ Found table for parsing")
        
        rows = table.find_all('tr')
        print(f"Found {len(rows)} rows")
        
        # Skip header row(s)
        data_rows = rows[1:] if len(rows) > 1 else rows
        
        for idx, row in enumerate(data_rows):
            try:
                cells = row.find_all(['td', 'th'])
                
                if len(cells) < 2:  # Need at least title and date
                    continue
                
                # Extract link
                link_elem = row.find('a')
                link = link_elem.get('href', '') if link_elem else ''
                
                # Make absolute URL if relative
                if link and not link.startswith('http'):
                    link = f"https://goir.ap.gov.in{link}" if link.startswith('/') else f"https://goir.ap.gov.in/{link}"
                
                announcement = {
                    'title': cells[0].text.strip() if len(cells) > 0 else '',
                    'date': cells[1].text.strip() if len(cells) > 1 else '',
                    'link': link,
                    'state': 'AndhraPradesh',
                    'description': cells[2].text.strip() if len(cells) > 2 else ''
                }
                
                # Only add if we have at least a title
                if announcement['title']:
                    announcements.append(announcement)
                    
            except Exception as e:
                print(f"⚠️ Error parsing row {idx}: {e}")
                continue
        
        print(f"✓ Successfully parsed {len(announcements)} announcements")
        
    except Exception as e:
        print(f"❌ Error in extract_announcements: {e}")
        import traceback
        traceback.print_exc()
    
    return announcements