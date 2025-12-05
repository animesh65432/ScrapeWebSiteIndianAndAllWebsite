from .utils import scrape_website
from config import config


async def GetHaryanaAnnoucements():
    try :
        print("Scraping Haryana Announcements...")
        return await scrape_website(config["Haryana"])
    except Exception as e :
        print("Error GetHaryanaAnnoucements",e)
        return None