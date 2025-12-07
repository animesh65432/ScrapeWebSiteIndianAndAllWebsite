from .utils import scrape_website
from config import NORTH_INDIA
async def GetPunjabAnnoucements():
    try :
        print("Scraping Punjab Announcements...")
        return await scrape_website(NORTH_INDIA["Punjab"])
    except Exception as e:
        print(f"GetPunjabAnnoucements error occurred: {str(e)}")
        return []