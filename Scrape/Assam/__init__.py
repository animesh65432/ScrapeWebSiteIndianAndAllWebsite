from .utils import scrape_website
from config import config
async def GetAssamAnnoucements():
    try :
        print("Scraping Assam Announcements...")
        return scrape_website(config["Assam"])
    except Exception as e:
        print("error in  Assam Announcements",e)
        return None