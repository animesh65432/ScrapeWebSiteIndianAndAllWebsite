from config import config
from .utils import scrape_website

async def scrape_ArunachalPradesh_Annoucements():
    try :
        return scrape_website(config["ArunachalPradesh"])
    except Exception as e :
        print("scrape_ArunachalPradesh_Annoucements Eroor",e)
        return None
        
    