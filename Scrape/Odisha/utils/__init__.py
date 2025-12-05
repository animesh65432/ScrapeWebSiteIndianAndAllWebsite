from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from datetime import datetime
from config.safe_quit import safe_quit
import asyncio

async def scapre_website(url: str):
    driver = None
    try:
        print("Odisha Scraping Started...", url)

        driver = await create_driver()

        if not await load_with_retry(driver, url, retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return None
        
        loop = asyncio.get_event_loop()

        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, 'html.parser')

        
        # ----------------------------
        # SAFE TABLE ACCESS
        # ----------------------------
        table = soup.find("table", {"class": "views-table sortable views-view-table cols-5"})
        if not table:
            print("ERROR: Odisha table not found!")
            return None

        tbody = table.find("tbody")
        if not tbody:
            print("ERROR: Odisha table BODY not found!")
            return None

        annoucements_lists = tbody.find_all("tr")
        if not annoucements_lists:
            print("ERROR: No rows found!")
            return None

        annocuements = []
        today = datetime.now().date()


        for annoucement in annoucements_lists:

            # ----------------------------
            # SAFE COLUMN ACCESS
            # ----------------------------
            title_col = annoucement.find("td", {"class": "views-field views-field-title"})
            date_col = annoucement.find("td", {"class": "views-field views-field-field-date"})
            link_col = annoucement.find("td", {"class": "views-field views-field-nothing"})

            if not title_col or not date_col or not link_col:
                continue   # skip incomplete rows

            title = title_col.get_text(strip=True)
            date_str = date_col.get_text(strip=True)

            # ----------------------------
            # PDF LINK SAFE ACCESS
            # ----------------------------
            link_tag = link_col.find("a")
            pdf_link = link_tag['href'] if link_tag else None

            if pdf_link and not pdf_link.startswith("http"):
                pdf_share = f"https://home.odisha.gov.in{pdf_link}"
            else:
                pdf_share = pdf_link

            # ----------------------------
            # SAFE DATE PARSING
            # ----------------------------
            try:
                date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
            except:
                continue  # skip invalid date rows

            # ----------------------------
            # FILTER BY TODAY
            # ----------------------------
            if date_obj != today:
                continue

            annocuements.append({
                "title": title,
                "pdf_link": pdf_share,
                "state": "Odisha"
            })

        return annocuements

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await safe_quit(driver=driver)
        return None
