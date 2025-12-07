from .utils import scrape_Website
from config import config

async def GetAllMaharashtraAnnoucements():
    try :
        print("Scraping Maharashtra Announcements...")
        return await scrape_Website(config["Maharashtra"])
    except Exception as e :
        print("GetAllMaharashtraAnnoucements",e)
        return []