from .utils import scrape_website
from config import config

async def GetjharkhandGovAnnoucements():
    try:
        print("Scraping Jharkhand Announcements...")
        scrape_website(config["jharkhand"])
    except Exception as e :
        print("Error in GetjharkhandGovAnnoucements",e)
        return None