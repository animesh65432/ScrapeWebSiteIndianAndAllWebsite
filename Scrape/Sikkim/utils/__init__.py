from bs4 import BeautifulSoup
from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options
from urllib.parse import urljoin
from datetime import datetime
from .scrape_content import scrape_content

BASE_URL = "https://www.sikkim.gov.in"

def scrape_website(url):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        table = soup.find("table", {"class": "table table-striped"})
        if not table:
            return "Table not found"

        rows = table.find_all("tr")

        announcements = []

        # Format today date same as website ("26 Nov 2025")
        today = datetime.today().strftime("%d %b %Y")

        for row in rows:
            strong_tag = row.find("strong")
            if not strong_tag:
                continue  # skip empty rows

            # Extract title
            title = strong_tag.get_text(strip=True)

            # Extract date: example -> "-26 Nov 2025"
            date_items = row.find_all("li")
            if len(date_items) >= 2:
                raw_date = date_items[1].get_text(strip=True)
                clean_date = raw_date.replace("-", "").strip()  # "26 Nov 2025"
            else:
                clean_date = ""

            # Skip if date is empty or does NOT match today
            if clean_date != today:
                continue

            # Extract link
            link_tag = row.find("a", href=True)
            if link_tag:
                link = urljoin(BASE_URL, link_tag["href"])
            else:
                link = None

            announcements.append({
                "title": title,
                "date": clean_date,
                "link": link
            })
        
        for announcement in announcements:
            if announcement['link']:
                content = scrape_content(announcement['link'])
                announcement['content'] = content
            else:
                announcement['content'] = None

        return announcements

    except Exception as e:
        return f"Error scraping Sikkim: {str(e)}"

    finally:
        driver.quit()
