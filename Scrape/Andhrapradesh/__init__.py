from config import config
from .utils import scrape_website

async def GetAndhrapradeshAnnoucements():
    try :
        return scrape_website(config["Andhrapradesh"])
    except Exception as e :
        print("GetAndhrapradeshAnnoucements",e)
        return None