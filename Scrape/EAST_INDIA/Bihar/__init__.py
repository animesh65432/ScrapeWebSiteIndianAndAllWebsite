from config import EAST_INDIA
from .utils import scrape_website

async def GetBiharAnnoucements():
    try :
        print("Scraping Bihar Announcements...")
        return await scrape_website(EAST_INDIA["Bihar"])
    except Exception as e :
        print("Error in GetBiharAnnoucements",e)
        return []