from config import config
from .utils import scrape_website

async def GetArunachalPradeshAnnoucements():
    try :
        print("Scraping ArunachalPradesh Announcements...")
        return await scrape_website(config["Arunachalpradesh"])
    except Exception as e :
        print("ArunachalPradesh_Annoucements Eroor",e)
        return None
        
    