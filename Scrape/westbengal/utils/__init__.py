from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

def scrape_website(url: str) -> dict:
    """
    Scrapes news items from a website containing a news table.
    
    Args:
        url: The URL to scrape
        
    Returns:
        dict: Contains success status, count, news items, or error message
    """
    try:
        # Setup headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # run without GUI
        chrome_options.add_argument("--ignore-certificate-errors")  # ignore SSL issues
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)

        # Open URL
        driver.get(url)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")

        # Find news table
        news_table = soup.find(id="ContentPlaceHolder1_grid_News")
        if not news_table:
            return {"success": False, "error": "News table not found", "news": []}

        news_items = []
        tbody = news_table.find("tbody")
        rows = tbody.find_all("tr") if tbody else news_table.find_all("tr")

        for row in rows:
            # Skip header rows
            if row.find("th"):
                continue

            # Extract date and content
            date_tag = row.find("h5", class_="text-primary")
            content_tag = row.find("p", class_="text-muted")
            date = date_tag.get_text(strip=True) if date_tag else ""
            content = content_tag.get_text(strip=True) if content_tag else ""

            # Validate date format (DD-MM-YYYY)
            if date and content and re.match(r"^\d{2}-\d{2}-\d{4}$", date):
                news_items.append({"date": date, "content": content})

        return {"success": True, "count": len(news_items), "news": news_items}

    except Exception as e:
        return {"success": False, "error": str(e), "news": []}
