from bs4 import BeautifulSoup
from datetime import datetime
from utils.fetch_with_httpx import fetch_with_httpx

async def scrape_website(url: str):
    try:

        html = await fetch_with_httpx(url=url)

        if not html:
            print("Failed to fetch page content")
            return []

        soup = BeautifulSoup(html, "html.parser")

        announcements = []

        for doc in soup.select(".documents"):
            title_element = doc.select_one(".documents_title a")
            if not title_element:
                continue
            title = title_element.get_text(strip=True)
            pdf_link = title_element.get("href", "")

            time_element = doc.select_one(".documents_date time")
            date_str = time_element.get_text(strip=True) if time_element else ""
            date_obj = datetime.strptime(date_str, "%d-%b-%Y").date()
            today = datetime.today().date()

            
            if date_obj != today:
                continue

            
            if title and pdf_link:
                full_pdf_url = f"https://assam.gov.in/{pdf_link.lstrip('/')}"
                announcements.append({
                    "title": title,
                    "pdf_link": full_pdf_url,
                    "state" :"Assam"
                })
        
        print(announcements)

        return announcements

    except Exception as e:
        print("Scraping Error:", str(e))
        return []
