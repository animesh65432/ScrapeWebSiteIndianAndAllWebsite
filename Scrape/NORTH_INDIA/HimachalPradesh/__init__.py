from .utils import scraping_website
from config import NORTH_INDIA


async def GetHimachalPradeshAnnoucements():
    try:
        print("Scraping HimachalPradesh Announcements...")
        return await scraping_website(NORTH_INDIA["HimachalPradesh"])
    except Exception as e : 
        print("Erro in GetHimachalPradesh",e)
        return []