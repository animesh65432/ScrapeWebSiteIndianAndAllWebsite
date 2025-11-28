from config import config
from .utils import scrape_website

async def GetAndamanNicobarIslandsAnnoucements():
    try :
        return scrape_website(config["AndamanNicobarIslands"])
    except Exception as e :
        print("GetAndamanNicobarIslandsAnnoucements",e)
        return None