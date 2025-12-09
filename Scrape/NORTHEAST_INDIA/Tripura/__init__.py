from .utils import scrape_website
from config import NORTHEAST_INDIA

async def GetAllTripuraAnnoucements():
    try :
        print("Scraping Tripura Announcements...")
        
        return await scrape_website(NORTHEAST_INDIA["Tripura"])
    except Exception as e :
        print("GetAllTripuraAnnoucements",e)
        return []