from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime,timedelta
from utils.load_with_retry import load_with_retry
from config.create_driver import create_driver
from config.safe_quit import safe_quit

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url=url, html_element=".col-lg-6", retries=3, delay=3):
            print("❌ Page failed to load after retries")
            await safe_quit(driver)
            return []

        wait = WebDriverWait(driver, 15)

        # Get all cards
        cards = driver.find_elements(By.CSS_SELECTOR, ".col-lg-6.col-md-6.col-12")

        results = []
        today = (datetime.today()-timedelta(days=5)).date()

        for card in cards:
            try:
                # Extract date
                date_text = card.find_element(By.CSS_SELECTOR, ".date p").text.strip()
                # Example: "02 Dec, 2025"
                date_obj = datetime.strptime(date_text, "%d %b, %Y").date()

                if date_obj != today:
                    continue

                # Extract title
                title = card.find_element(By.CSS_SELECTOR, ".notification-heading p").text.strip()

                # Extract PDF link if exists
                link_tag = card.find_elements(By.CSS_SELECTOR, ".notification-item")
                pdf_link = None

                if link_tag:
                    link = link_tag[0].get_attribute("href")
                    if link.startswith("/"):
                        pdf_link = "https://cgstate.gov.in" + link
                    else:
                        pdf_link = link

                results.append({
                    "title": title,
                    "pdf_link": pdf_link,
                    "state": "Chhattisgarh"
                })

            except Exception as e:
                print("Card processing error:", e)
                continue

        await safe_quit(driver)
        return results

    except Exception as e:
        print("Scraping Error:", e)
        await safe_quit(driver)
        return []
