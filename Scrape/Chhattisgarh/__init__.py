from .utils import scrape_website
from config import config

async def ScrapeChhattisgarhAnnoucement():
    try :
        return scrape_website(config["ArunachalPradesh"])
    except Exception as e :
        print("GetChhattisgarhAnnoucement Error",e)
        return None