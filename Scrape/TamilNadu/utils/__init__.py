from datetime import datetime
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from config.safe_quit import safe_quit
import asyncio


def parse_tn_date(date_str: str):
    """
    Converts 'November 27 ,2025' → datetime.date(2025, 11, 27)
    """
    date_str = date_str.replace(" ,", " ")  
    return datetime.strptime(date_str, "%B %d %Y").date()


async def scrape_website(url):
    driver = None
    try:
        driver = await create_driver()
        
        if await load_with_retry(driver, url, html_element=".list-group.pr-list-group",retries=3, delay=3) is False:
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return None
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, "html.parser")



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
                "pdf_link": pdf_link,
                "state": "TamilNadu"
            })

        return announcements

    except Exception as e:
        await safe_quit(driver=driver)
        print("scrape_website error in TamilNadu utils:", e)
        return None
