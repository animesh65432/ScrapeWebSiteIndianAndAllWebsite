from .utils import scarp_website
from config import GovtWebiteUrl

async def GetNagalandAnnoucements():
    try :
        return scarp_website(GovtWebiteUrl["Nagaland"])
    except Exception as e:
        return f"GetNagalandAnnoucements error occurred: {str(e)}"