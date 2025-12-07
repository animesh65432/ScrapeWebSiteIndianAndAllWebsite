from .utils import scraping_website
from config import config


async def GetHimachalPradeshAnnoucements():
    try:
        print("Scraping HimachalPradesh Announcements...")
        return await scraping_website(config["HimachalPradesh"])
    except Exception as e : 
        print("Erro in GetHimachalPradesh",e)
        return None