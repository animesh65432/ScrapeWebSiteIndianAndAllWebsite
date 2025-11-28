from config import config
from .utils import scrape_website

async def GetBiharAnnoucements():
    try :
        return scrape_website(config["Bihar"])
    except Exception as e :
        print("GetBiharAnnoucements",e)
        return None