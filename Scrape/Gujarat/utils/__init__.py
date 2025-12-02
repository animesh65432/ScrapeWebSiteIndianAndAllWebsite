from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_website(url):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        
        table = soup.find("table", {"class": "tableData DocumentTable"})

        if not table:
            print("Table not found")
            return None

        rows = table.find("tbody").find_all("tr")
        announcements = []
        today = datetime.today().date()

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 6:
                continue

            title = cols[4].get_text(strip=True)
            date_str = cols[2].get_text(strip=True)  # E.g., 03/03/2025

            # Skip blank dates
            if not date_str or date_str == "-":
                continue

            try:
                date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()

                if date_obj == today:
                    pdf_link = None
                    link_tag = cols[5].find("a")
                    if link_tag:
                        pdf_link = link_tag.get("href")

                    announcements.append({
                        'title': title,
                        'pdf_link':f"https://gad.gujarat.gov.in/personnel/{pdf_link}",
                        'state': "Gujarat"
                    })

            except Exception as e:
                print(f"Invalid date format: {date_str} - {e}")
                continue

        print(f"\nTotal announcements matching today's date: {len(announcements)}")
        return announcements

    except Exception as e:
        print("scrape_website", e)
        return None
