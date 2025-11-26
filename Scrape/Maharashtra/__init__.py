from .utils import scrape_Website
from config import config

async def GetAllMaharashtraAnnoucements():
    try :
        return scrape_Website(config["Maharashtra"])
    except Exception as e :
        print("GetAllMaharashtraAnnoucements",e)