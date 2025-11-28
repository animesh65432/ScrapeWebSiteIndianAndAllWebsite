from .utils import scrape_website
from config import GovtWebiteUrl

async def GetMizoramAnnoucements():
    try :
        return scrape_website(GovtWebiteUrl["Mizoram"])
    except Exception as e:
        return f"GetMizoramAnnoucements error occurred: {str(e)}"