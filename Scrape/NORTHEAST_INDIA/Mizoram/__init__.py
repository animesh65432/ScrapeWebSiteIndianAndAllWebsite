from .utils import scrape_website
from config import NORTHEAST_INDIA

async def GetMizoramAnnoucements():
    try :
        print("Scraping Mizoram Announcements...")
        return await scrape_website(NORTHEAST_INDIA["Mizoram"])
    except Exception as e:
        print(f"GetMizoramAnnoucements error occurred: {str(e)}")
        return []