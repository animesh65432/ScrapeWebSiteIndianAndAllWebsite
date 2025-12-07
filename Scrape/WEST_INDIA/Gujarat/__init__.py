from .utils import scrape_website
from config import config

async def GetGujaratAnnoucements():
    try :
        print("Scraping Gujarat Announcements...")
        return await scrape_website(config["Gujarat"])
    except Exception as e :
        print("Error GetGujaratAnnoucements",e)
        return []