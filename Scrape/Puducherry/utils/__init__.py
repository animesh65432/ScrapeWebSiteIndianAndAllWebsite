from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        items_lists = soup.find("div", {"class": "view-content"}) \
                          .find("div", {"class": "item-list"}) \
                          .find_all("li")

        announcements = []

        today = datetime.today().date() 

        for item in items_lists:
            title = item.find("div", {"class": "views-field views-field-title"}) \
                        .find("span", {"class": "field-content"}) \
                        .get_text(strip=True)

            date_str = item.find("span", {"class": "date-display-single"}).get_text(strip=True)

            try:
                item_date = datetime.strptime(date_str, "%d/%m/%Y").date()
            except ValueError:
                print(f"Date parse error: {date_str}")
                continue

            pdf_div = item.find("div", {"class": "views-field views-field-field-upload-pdf"})
            pdf_link = pdf_div.find("a")['href'] if pdf_div and pdf_div.find("a") else None

            # Compare date objects (correct!)
            if item_date == today and pdf_link:
                announcements.append({
                    "title": title,
                    "date": date_str,
                    "pdf": pdf_link
                })

        return announcements

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
