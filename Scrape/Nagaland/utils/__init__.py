from datetime import datetime,timedelta
from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup

def scarp_website(url: str):
    try:
        # Setup Chrome
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Parse HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Find table rows
        table_body = soup.find("table").find("tbody")
        announcement_rows = table_body.find_all("tr")

        # Today's date in the format used in the table
        today_str = (datetime.today() - timedelta(days=141) ).strftime("%d-%m-%Y")

        print(today_str)

        today_announcements = []

        for row in announcement_rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            serial = cols[0].text.strip()
            title_tag = cols[1].find("a")
            title = title_tag.text.strip() if title_tag else cols[1].text.strip()
            category = cols[2].text.strip()
            date = cols[3].text.strip()
            link_tag = cols[4].find("a")
            link = link_tag['href'] if link_tag else (f"{url}{title_tag['href']}" if title_tag else "")
            if link.startswith("/"):
                link = f"{url}{link}"

            if date == today_str and title and link:
                today_announcements.append({
                    "title": title,
                    "category": category,
                    "link": link
                })

        return today_announcements

    except Exception as e:
        return f"An error occurred: {str(e)}"
