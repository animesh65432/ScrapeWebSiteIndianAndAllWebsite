from datetime import datetime ,timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config.chromeOptions import Get_Chrome_Options
from .scarpeContent import scrape_content
import re

def scrape_website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        WebDriverWait(driver, 25).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".card .card-body")))


        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.find_all("div", {"class": "card"})

        announcements = []
        today = datetime.today().date() - timedelta(days=2)

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
                desc_elem = card_body.find("p", {"class": "card-text"})
                link_elem = card_body.find("a", {"class": "btn btn-primary"})

                announcements.append({
                    "title": title_elem.text.strip() if title_elem else "No title",
                    "description": desc_elem.text.strip() if desc_elem else "No description",
                    "link": link_elem.get("href") if link_elem else None,
                })

            except Exception as card_error:
                print(f"Error parsing card: {card_error}")
                continue
        
        for i in range(len(announcements)):
            announcements[i]["content"] = scrape_content(announcements[0]["link"])
        
        return announcements

    except Exception as e:
        print(f"Error scraping website: {e}")
        return None
