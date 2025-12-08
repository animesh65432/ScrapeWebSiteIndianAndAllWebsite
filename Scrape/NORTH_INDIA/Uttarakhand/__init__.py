from .utils import scrape_website
from config import NORTH_INDIA

async def GetUttarakhandAnnouncements():
    try :
        print("Scraping Uttarakhand Announcements...")
        return await scrape_website(NORTH_INDIA["Uttarakhand"])
    except Exception as e :
        print("GetUttarakhandAnnouncements",e)
        return []