from bs4 import BeautifulSoup
from datetime import datetime
from utils.hindi_months import hindi_months
from ..utils import scrape_content
from  utils.fetch_with_httpx import fetch_with_httpx

async def scrape_website(url: str):
    try:
        print(f"Loading Madhya Pradesh page: {url}")

        html = await fetch_with_httpx(url,part="central_India")        
        
        soup = BeautifulSoup(html, 'html.parser')


        table = soup.find('table', {"class" :"table table-striped table-bordered"})

        announcements_html_lists = table.find('tbody').find_all('tr')

        announcements = []

        for ann in announcements_html_lists:
            title = ann.find_all('td')[1].text.strip()
            date_str = ann.find_all('td')[2].text.strip()
            date_parts = date_str.replace(",", "").split()
            month = hindi_months[date_parts[1]]
            day = int(date_parts[2])
            year = int(date_parts[3])
            time_str = date_parts[4]
            dt = datetime.strptime(f"{day}-{month}-{year} {time_str}", "%d-%m-%Y %H:%M")
            today = datetime.now()
            link = ann.find_all('td')[1].find('a')['href'].strip()

            if today.date() == dt.date() and title and link:
                announcement = {
                    "title": title,
                    "link": link,
                    "state": "MadhyaPradesh",
                    "content": await scrape_content(link) 
                }

                announcements.append(announcement)
        
        return announcements
    except Exception as e:
        print(f"scrape_madhya_pradesh error: {e}")
        return []

