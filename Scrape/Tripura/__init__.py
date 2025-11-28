from .utils import scrape_website
from config import config

async def GetAllTripuraAnnoucements():
    try :
        return scrape_website(config["Tripura"])
    except Exception as e :
        print("GetAllTripuraAnnoucements",e)
        return None