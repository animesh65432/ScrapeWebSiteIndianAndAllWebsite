from .utils import scrape_website
from config import config

async def GetKarnatakaGovtAnnoucements():
    try :
        return scrape_website(config["Karnataka"])
    except Exception as e :
        print("Error in etKarnataka_Govt_Annoucements",e)