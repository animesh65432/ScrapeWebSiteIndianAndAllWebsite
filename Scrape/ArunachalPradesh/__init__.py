from config import config
from .utils import scrape_website

async def GetArunachalPradeshAnnoucements():
    try :
        return scrape_website(config["Arunachalpradesh"])
    except Exception as e :
        print("scrape_ArunachalPradesh_Annoucements Eroor",e)
        return None
        
    