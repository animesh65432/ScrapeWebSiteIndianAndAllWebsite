from .utils import scrape_website
from config import config

async def GetPuducherryAnnoucements():
    try :
        print("Scraping Puducherry Announcements...")
        return await scrape_website(config["Puducherry"])
    except Exception as e:
        print(f"GetPuducherryAnnoucements error occurred: {str(e)}")
        return []