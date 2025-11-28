from config import config
from .utils import scrape_website

async def GetChandigrahAnnoucements():
    try :
        return scrape_website(config["Chandigarh"])
    except Exception as e :
        print("GetChandigarhAnnoucements",e)
        return None