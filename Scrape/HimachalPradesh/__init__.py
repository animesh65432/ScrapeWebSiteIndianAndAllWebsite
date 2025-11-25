from .utils import scraping_website
from config import config


async def scapre_HimachalPradesh_Annoucements():
    try:
        return scraping_website(config["HimachalPradesh"])
    except Exception as e : 
        print("Erro in GetHimachalPradesh",e)
        return None