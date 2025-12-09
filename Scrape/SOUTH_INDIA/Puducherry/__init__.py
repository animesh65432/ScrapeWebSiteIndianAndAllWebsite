from .utils import scrape_website
from config import SOUTH_INDIA

async def GetPuducherryAnnoucements():
    try :
        print("Scraping Puducherry Announcements...")
        return await scrape_website(SOUTH_INDIA["Puducherry"])
    except Exception as e:
        print(f"GetPuducherryAnnoucements error occurred: {str(e)}")
        return []