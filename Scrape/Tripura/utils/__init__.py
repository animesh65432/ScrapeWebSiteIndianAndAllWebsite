from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta
from config.chromeOptions import Get_Chrome_Options
import re

def scrape_website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        announcements = []

        table = soup.find("table", class_="table table-bordered table-hover cols-3")
        if not table:
            return []

        rows = table.find("tbody").find_all("tr")

        today = (datetime.today() - timedelta(days=11)).date()

        for row in rows:

           
            title_cell = row.find("td", class_="views-field-title")
            if not title_cell:
                continue

            title = title_cell.get_text(strip=True)

            print(title)

            # Extract "Dated 15th November, 2025"
            match = re.search(r"Dated\s+(\d{1,2}(st|nd|rd|th)?\s+\w+,\s+\d{4})", title)
            if not match:
                continue

            date_str = match.group(1)

            # Remove st/nd/rd/th
            cleaned = re.sub(r"(st|nd|rd|th)", "", date_str)

           
            parsed_date = datetime.strptime(cleaned.strip(), "%d %B, %Y").date()

            link_cell = row.find("td", class_="views-field-field-upload-pdf")
            if not link_cell:
                continue

            link = link_cell.find("a")["href"]
            if link.startswith("/"):
                link = "https://tripura.gov.in" + link

            if parsed_date == today:
                announcements.append({
                    "title": title,
                    "link": link
                })

        return announcements

    except Exception as e:
        return f"scrape_website error occurred: {str(e)}"
