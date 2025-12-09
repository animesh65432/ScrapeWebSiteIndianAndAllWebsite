from .utils import scrape_website
from config import EAST_INDIA

async def GetjharkhandGovAnnoucements():
    try:
        print("Scraping Jharkhand Announcements...")
        return await scrape_website(EAST_INDIA["jharkhand"])
    except Exception as e :
        print("Error in GetjharkhandGovAnnoucements",e)
        return []