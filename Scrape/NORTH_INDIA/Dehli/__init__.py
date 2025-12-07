from .utils import scrape_website
from config import NORTH_INDIA

async def GetDehliAnnoucements():
    try:
        print("Scraping Dehli Announcements...")
        return await scrape_website(NORTH_INDIA["Dehli"])
    except Exception as e:
        print("Error in Dehli Scraping",e)
        return []