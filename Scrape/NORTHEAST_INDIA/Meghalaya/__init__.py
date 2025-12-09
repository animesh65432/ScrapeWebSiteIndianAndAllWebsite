from .utils import scapre_website
from config import NORTHEAST_INDIA


async def GetmeghalayaAnnoucements():
    try :
        print("Scraping Meghalaya Announcements...")
        
        return await scapre_website(NORTHEAST_INDIA["Meghalaya"])
    except Exception as e:
        print(f"GetmeghalayaAnnoucements error occurred: {str(e)}")

        return []