from .utils import scrape_website
from config import GovtWebiteUrl
async def GetKeralaGovtAnnoucements():
    try :
        return scrape_website(GovtWebiteUrl["Kerala"])
    except Exception as e : 
        print("GetKeralaGovtAnnoucements",e)
        return None
