from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from config.chromeOptions import Get_Chrome_Options

def scrape_website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")

        table = soup.select_one("table.data-table-1.doc-table.bt")
        if not table:
            print("No table found")
            return []

        rows = table.find("tbody").find_all("tr")

        today = datetime.today().date()  # today

        announcements = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            title = cols[0].get_text(strip=True)

            date_text = cols[1].get_text(strip=True)  # "26/11/2025"
            parsed_date = datetime.strptime(date_text, "%d/%m/%Y").date()

            # Skip if not today
            if parsed_date != today:
                continue

            # Get PDF link
            link_tag = cols[2].find("a", href=True)
            link = link_tag["href"] if link_tag else None


            announcements.append({
                "title": title,
                "pdf_link": link,
                "state": "Ladakh"
            })

        return announcements

    except Exception as e:
        print(f"Error: {e}")
        return None
