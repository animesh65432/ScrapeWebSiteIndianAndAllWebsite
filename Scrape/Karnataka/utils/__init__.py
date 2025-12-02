from datetime import datetime
from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

def scrape_website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "table-striped table-bordered table"})
        
        if not table:
            print("Table not found!")
            return []

        notices = []

        rows = table.find("tbody").find_all("tr")

        for row in rows[1:]:     
            cells = row.find_all("td")
            date_str = cells[2].get_text(strip=True)
            subject = cells[3].get_text(strip=True)

            
            try:
                scraped_date = datetime.strptime(date_str, "%d-%m-%Y").date()
            except:
                continue  # skip invalid dates
            
            
            if scraped_date != datetime.today().date():
                continue   # skip anything not today

            view_link = cells[5].find("a")
            view_url = None

            if view_link:
                href = view_link.get("href")
                if href:
                    view_url = urljoin("https://egovernance.karnataka.gov.in/", href)

            if view_url:
                notices.append({
                    "date": date_str,
                    "title": subject,
                    "pdf_link": view_url
                })

        return notices

    except Exception as e:
        print("Scraping Error:", str(e))
        return []
