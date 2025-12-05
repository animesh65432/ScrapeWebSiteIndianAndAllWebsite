from .utils import scrape_website
from config import config

async def GetAllTripuraAnnoucements():
    try :
        print("Scraping Tripura Announcements...")
        
        return await scrape_website(config["Tripura"])
    except Exception as e :
        print("GetAllTripuraAnnoucements",e)
        return None