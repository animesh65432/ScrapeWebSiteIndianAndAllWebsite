from .utils import scrape_website
from config import SOUTH_INDIA

async def GetAllTelanganaAnnoucements():
    try :
        print("Scraping Telangana Announcements...")
        
        return await scrape_website(SOUTH_INDIA["Telangana"])
    except Exception as e :
        print("GetAllTelanganaAnnoucements",e)
        return []