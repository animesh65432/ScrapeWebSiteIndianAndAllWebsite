from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from utils.load_with_retry import load_with_retry
from config.create_driver import create_driver
from config.safe_quit import safe_quit
import time
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()
        datestart = datetime.now() - timedelta(days=1)
        dateend = datetime.now()
        start_str = datestart.strftime("%Y-%m-%d")
        end_str = dateend.strftime("%Y-%m-%d")

        final_url = f"{url}&dateFrom={start_str}&dateTo={end_str}"

        if not await load_with_retry(driver, final_url,html_element="#modalNotificationDetails table.custom-table" ,retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            safe_quit(driver=driver)
            return []

        
        wait = WebDriverWait(driver, 10)
        view_all_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "notification-item-view"))
        )
        view_all_button.click()

        # Wait for the modal to appear and content to load
        modal = wait.until(
            EC.visibility_of_element_located((By.ID, "notificationModal"))
        )
        
        # Wait for the table to load inside the modal
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "custom-table"))
        )
        
        # Give extra time for dynamic content
        time.sleep(2)

        # Get the page source after modal loads
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, "html.parser")

        # Find the modal and extract data
        modal_body = soup.find("div", id="modalNotificationDetails")
        
        if modal_body:
            table = modal_body.find("table", class_="custom-table")
            
            if table:
                results = []
                rows = table.find("tbody").find_all("tr")
                
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 4:
                        publish_date = cols[0].get_text(strip=True)
                        title = cols[1].get_text(strip=True)
                        
                        download_cell = cols[3]
                        pdf_link = None
                        link_tag = download_cell.find("a", href=True)

                        date_obj = datetime.strptime(publish_date, "%d %b, %Y").date()
                        
                        today = datetime.today().date()

                        if link_tag:
                            pdf_link = link_tag['href']
                            if pdf_link.startswith('/'):
                                pdf_link = f"https://cgstate.gov.in{pdf_link}"
 
                        if date_obj == today :
                            results.append({
                                "title": title,
                                "pdf_link": pdf_link,
                                "state" :"Chhattisgarh"
                            })
                
                return results
            else:
                print("No table found in modal")
        else:
            print("Modal body not found")

        return []

    except Exception as e:
        print("Scraping Error:", str(e))
        await safe_quit(driver=driver)
        return []
