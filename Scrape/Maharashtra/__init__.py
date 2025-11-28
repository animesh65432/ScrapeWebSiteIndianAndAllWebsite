from .utils import scrape_Website
from config import GovtWebiteUrl

async def GetAllMaharashtraAnnoucements():
    try :
        return scrape_Website(GovtWebiteUrl["Maharashtra"])
    except Exception as e :
        print("GetAllMaharashtraAnnoucements",e)