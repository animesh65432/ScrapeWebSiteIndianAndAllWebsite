from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime ,timedelta
from .scarpContent import scarpContent
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()
    
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element((By.CSS_SELECTOR, "app-mini-loader .mini-loading"))
        )

        if not await load_with_retry(driver, url, html_element="table",retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []

        # Now page is fully loaded
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"class": "table font-14 table-striped table_order_list table-custom table-custom"})

        announcements = []

        # Get current date components
        current_day = (datetime.now() - timedelta(days=1)).day
        
        # Month mapping from English to Hindi
        months_hindi = {
            1: "जनवरी", 2: "फरवरी", 3: "मार्च", 4: "अप्रैल",
            5: "मई", 6: "जून", 7: "जुलाई", 8: "अगस्त",
            9: "सितम्बर", 10: "अक्टूबर", 11: "नवम्बर", 12: "दिसम्बर"
        }
        
        current_month = months_hindi[datetime.now().month]
        current_year = datetime.now().year
        
        # Format: "28 नवम्बर 2025"
        today_date_str = f"{current_day} {current_month} {current_year}"

        announcements_lists = table.find("tbody").find_all("tr")

        for announcement in announcements_lists:
            tds = announcement.find_all("td")
            
            if len(tds) >= 4:
                date_time = tds[1].get_text(strip=True)
                title = tds[2].get_text(strip=True)
                detail_link = tds[3].find("a")
                
                # Extract just the date part (before comma)
                date_part = date_time.split(",")[0].strip()
                
                # Check if the date matches today's date

                if detail_link :
                    link = f"https://dipr.rajasthan.gov.in" + detail_link['href']
                    content = await scarpContent(link)


                if date_part == today_date_str and detail_link and content:
                    announcement_data = {
                        "title": title,
                        "state": "Rajasthan",
                        "link": link ,
                        "content": content
                    }
                    announcements.append(announcement_data)
      
    
        return announcements

    except Exception as e:
        print(f"Error in scrape_website: {e}")
        await safe_quit(driver=driver)
        return []