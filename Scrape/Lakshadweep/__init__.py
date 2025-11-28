from config import config
from .utils import scrape_website

async def GetLaskhadweepAnnoucements():
    try :
        return scrape_website(config["Lakshadweep"])
    except Exception as e :
        print("GetLakshadweepAnnoucements",e)
        return None