from .utils import scrape_website
from config import config

async def GetMizoramAnnoucements():
    try :
        print("Scraping Mizoram Announcements...")
        return await scrape_website(config["Mizoram"])
    except Exception as e:
        return f"GetMizoramAnnoucements error occurred: {str(e)}"