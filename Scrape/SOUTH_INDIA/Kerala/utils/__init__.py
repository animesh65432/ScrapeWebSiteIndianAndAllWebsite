from datetime import datetime 
from utils.load_with_retry import load_with_retry
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config.create_driver import create_driver
from .scarpeContent import scrape_content
import re
from  config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:

        driver = await create_driver()
        
        if not await load_with_retry(driver, url,html_element = ".card",part="south_india" ,retries=3, delay=3,isdymainc=True):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        WebDriverWait(driver, 25).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".card .card-body")))

        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.find_all("div", {"class": "card"})

        announcements = []
        today = datetime.today().date()

        for card in cards:
            try:
                card_body = card.find("div", {"class": "card-body"})
                if not card_body:
                    continue

                # Extract date text
                date_elem = card_body.find("small")
                if not date_elem:
                    continue

                date_text = date_elem.get_text(strip=True)

                # Extract only YYYY-MM-DD
                match = re.findall(r"\d{4}-\d{2}-\d{2}", date_text)
                if not match:
                    continue

                extracted_date = match[0]
                parsed_date = datetime.strptime(extracted_date, "%Y-%m-%d").date()

                # ❗ Skip announcements not from today
                if parsed_date != today:
                    continue

                # Extract other fields
                title_elem = card_body.find("h5", {"class": "card-title"})
                
                link_elem = card_body.find("a", {"class": "btn btn-primary"})
                link = link_elem.get("href")

                if not link:
                    continue


                announcements.append({
                    "title": title_elem.text.strip() if title_elem else "No title",
                    "link": link,
                    "state": "Kerala",
                    "content": await scrape_content(link)
                })

            except Exception as card_error:
                print(f"Error parsing card: {card_error}")
                continue
        
        return announcements

    except Exception as e:
        print(f"Error scraping website: {e}")
        await safe_quit(driver=driver)
        return []
