from config import config
from .utils import scrape_website

async def GetBiharAnnoucements():
    try :
        print("Scraping Bihar Announcements...")
        return scrape_website(config["Bihar"])
    except Exception as e :
        print("Erro in GetBiharAnnoucements",e)
        return None