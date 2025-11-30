from .utils import scrape_website
from config import config

async def GetAllTelanganaAnnoucements():
    try :
        print("Scraping Telangana Announcements...")
        
        return scrape_website(config["Telangana"])
    except Exception as e :
        print("GetAllTelanganaAnnoucements",e)
        return None