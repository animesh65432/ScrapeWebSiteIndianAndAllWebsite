import os
from datetime import datetime
from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup


def parse_tn_date(date_str: str):
    """
    Converts 'November 27 ,2025' → datetime.date(2025, 11, 27)
    """
    date_str = date_str.replace(" ,", " ")  
    return datetime.strptime(date_str, "%B %d %Y").date()


def scrape_website(url):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        announcements = []

        announcements_html_lists = soup.find("ul", {"class": "list-group pr-list-group"}).find_all("li")

        today = datetime.today().date()

        for item in announcements_html_lists:

            # Extract title
            title_tag = item.find("p", {"class": "list-group-item-text"})
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            # Extract date
            date_tag = item.find("div", {"class": "tag tag--blue"})
            if not date_tag:
                continue

            date_str = date_tag.find("span", {"class": "tag-label"}).get_text(strip=True)
            date_str = date_str.replace("\xa0", "").strip()  # clean spaces

            try:
                date_obj = parse_tn_date(date_str)
            except:
                continue  # skip if date invalid

            # Only process if date == today
            if date_obj != today:
                continue

            # Extract PDF link
            pdf_link_tag = item.find("a", href=True)
            if not pdf_link_tag:
                continue

            pdf_link = pdf_link_tag["href"]

            # Must be PDF
            if not pdf_link.lower().endswith(".pdf"):
                continue

            # Add to announcements array
            announcements.append({
                "title": title,
                "date": str(date_obj),
                "link": pdf_link
            })

        return announcements

    except Exception as e:
        print("scrape_website error in TamilNadu utils:", e)
        return None
