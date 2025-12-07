from config import NORTHEAST_INDIA
from .utils import scrape_website

async def GetArunachalPradeshAnnoucements():
    try :
        print("Scraping ArunachalPradesh Announcements...")
        return await scrape_website(NORTHEAST_INDIA["Arunachalpradesh"])
    except Exception as e :
        print("ArunachalPradesh_Annoucements Eroor",e)
        return []
        
    