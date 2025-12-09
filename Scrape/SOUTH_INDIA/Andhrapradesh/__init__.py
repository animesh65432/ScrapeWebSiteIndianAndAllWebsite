from config import SOUTH_INDIA
from .utils import scrape_website

async def GetAndhrapradeshAnnoucements():
    try :
        print("Scraping Andhrapradesh Announcements...")
        return await scrape_website(SOUTH_INDIA["Andhrapradesh"])
    except Exception as e :
        print("Error in GetAndhrapradeshAnnoucements",e)
        return []