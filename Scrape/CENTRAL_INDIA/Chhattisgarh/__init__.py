from .utils import scrape_website
from config import config

async def GetChhattisgarhAnnoucement():
    try :
        print("Scraping Chhattisgarh Announcements...",config["Chhattisgarh"])
        return await scrape_website(config["Chhattisgarh"])
    except Exception as e :
        print("GetChhattisgarhAnnoucement Error",e)
        return []