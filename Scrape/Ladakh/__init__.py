from .utils import scrape_website
from config import config
async def GetAllLadakhAnnoucements():
    try :
        print("Scraping Ladakh Announcements...")
        return await scrape_website(config["Ladakh"])
    except Exception as e :
        print("GetAllLadakhAnnoucements",e)