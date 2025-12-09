from .utils import scarp_website
from config import NORTHEAST_INDIA

async def GetNagalandAnnoucements():
    try :
        print("Scraping Nagaland Announcements...")
        return await scarp_website(NORTHEAST_INDIA["Nagaland"])
    except Exception as e:
        print(f"GetNagalandAnnoucements error occurred: {str(e)}")
        return []