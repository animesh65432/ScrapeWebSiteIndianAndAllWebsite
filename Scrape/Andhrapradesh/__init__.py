from config import config
from .utils import scrape_website

async def GetAndhrapradeshAnnoucements():
    try :
        print("Scraping Andhrapradesh Announcements...")
        return scrape_website(config["Andhrapradesh"])
    except Exception as e :
        print("Error in GetAndhrapradeshAnnoucements",e)
        return None