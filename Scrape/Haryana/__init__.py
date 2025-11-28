from .utils import scrape_website
from config import config


async def GetHaryanaAnnoucements():
    try :
        return scrape_website(config["Haryana"])
    except Exception as e :
        print("GetHaryanaAnnoucements",e)
        return None