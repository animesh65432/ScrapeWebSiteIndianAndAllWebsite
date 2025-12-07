from .utils import scrape_website
from config import NORTH_INDIA


async def GetHaryanaAnnoucements():
    try :
        print("Scraping Haryana Announcements...")
        return await scrape_website(NORTH_INDIA["Haryana"])
    except Exception as e :
        print("Error GetHaryanaAnnoucements",e)
        return []