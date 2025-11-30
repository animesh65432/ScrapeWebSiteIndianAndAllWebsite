from config import config
from .utils import scrape_website

async def GetAllMadhyaPradeshAnnoucements():
    try :
        print("Scraping MadhyaPradesh Announcements...")
        return scrape_website(config["MadhyaPradesh"])
    except Exception as e :
        print("GetAllMadhyaPradeshAnnoucements",e)