from config import config
from.utils import scarpe_website

async def GetUttarPradeshAnnoucements():
    try :
        return scarpe_website(config["UttarPradesh"])
    except Exception as e :
        print("GetUttarPradeshAnnoucements",e)
        return None