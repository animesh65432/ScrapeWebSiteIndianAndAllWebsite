from .utils import scarp_website
from config import config

async def GetNagalandAnnoucements():
    try :
        return scarp_website(config["Nagaland"])
    except Exception as e:
        return f"GetNagalandAnnoucements error occurred: {str(e)}"