from .utils import scrape_website
from config import config

async def GetDehliAnnoucements():
    try:
        print("Scraping Dehli Announcements...")
        return await scrape_website(config["Dehli"])
    except Exception as e:
        print("Error in Dehli Scraping",e)
        return None