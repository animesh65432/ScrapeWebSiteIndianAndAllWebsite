from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options
from bs4 import BeautifulSoup
import re
from datetime import datetime

def scrape_website(url: str) -> dict:
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")

        news_table = soup.find(id="ContentPlaceHolder1_grid_News")
        if not news_table:
            return {"success": False, "error": "News table not found", "news": []}

        news_items = []
        tbody = news_table.find("tbody")
        rows = tbody.find_all("tr") if tbody else news_table.find_all("tr")
        
        today = datetime.now().date()

        for row in rows:
            if row.find("th"):
                continue

            date_tag = row.find("h5", class_="text-primary")
            content_tag = row.find("p", class_="text-muted")

            date_str = date_tag.get_text(strip=True) if date_tag else ""
            content = content_tag.get_text(strip=True) if content_tag else ""

            # Validate date string format
            if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_str):
                continue

            news_date = datetime.strptime(date_str, "%d-%m-%Y").date()

            if news_date == today and content:
                news_items.append({
                    "content": content,
                    "state": "WestBengal",
                    "link": url
                })

        return news_items

    except Exception as e:
        print(f"scrape_website error: {e}")
        return None
