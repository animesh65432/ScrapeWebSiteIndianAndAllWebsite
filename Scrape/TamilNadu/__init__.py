from config import config
from .utils import scrape_website

async def GetallTamilNaduAnnoucements():
    try :
        return scrape_website(config["TamilNadu"])
    except Exception as e :
        print("GetallTamilNaduAnnoucements",e)
        return None