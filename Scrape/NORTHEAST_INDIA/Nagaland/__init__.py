from .utils import scarp_website
from config import config

async def GetNagalandAnnoucements():
    try :
        print("Scraping Nagaland Announcements...")
        return await scarp_website(config["Nagaland"])
    except Exception as e:
        print(f"GetNagalandAnnoucements error occurred: {str(e)}")
        return []