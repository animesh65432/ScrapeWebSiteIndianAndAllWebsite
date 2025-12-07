from .utils import scapre_website
from config import config


async def GetmeghalayaAnnoucements():
    try :
        print("Scraping Meghalaya Announcements...")
        
        return await scapre_website(config["Meghalaya"])
    except Exception as e:
        return f"GetmeghalayaAnnoucements error occurred: {str(e)}"