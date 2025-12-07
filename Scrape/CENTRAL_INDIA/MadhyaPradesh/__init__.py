from config import CENTRAL_INDIA
from .utils import scrape_website

async def GetAllMadhyaPradeshAnnoucements():
    try :
        print("Scraping MadhyaPradesh Announcements...")
        return await scrape_website(CENTRAL_INDIA["MadhyaPradesh"])
    except Exception as e :
        print("GetAllMadhyaPradeshAnnoucements errors ",e)
        return []