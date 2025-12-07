from .utils import scrape_website
from config import EAST_INDIA
async def GetwestBengalAnnoucements():
    try :
        return await scrape_website(EAST_INDIA["WestBengal"])
    except Exception as e:
        print("error in  scarpe_westBengal",e)
        return []