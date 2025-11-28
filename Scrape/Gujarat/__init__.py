from .utils import scrape_website
from config import config

async def GetGujaratAnnoucements():
    try :
        return scrape_website(config["Gujarat"])
    except Exception as e :
        print("GetGujaratAnnoucements",e)
        return None