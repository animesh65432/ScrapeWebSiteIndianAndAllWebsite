from .utils import scrape_website
from config import config
async def GetPunjabAnnoucements():
    try :
        print("Scraping Punjab Announcements...")
        return scrape_website(config["Punjab"])
    except Exception as e:
        return f"GetPunjabAnnoucements error occurred: {str(e)}"