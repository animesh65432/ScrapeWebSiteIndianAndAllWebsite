from config import WEST_INDIA
from .utils import scrape_website

async def GetBiharAnnoucements():
    try :
        print("Scraping Bihar Announcements...")
        return await scrape_website(WEST_INDIA["Bihar"])
    except Exception as e :
        print("Erro in GetBiharAnnoucements",e)
        return []