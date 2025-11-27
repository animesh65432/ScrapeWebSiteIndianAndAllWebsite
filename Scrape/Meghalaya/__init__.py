from .utils import scapre_website
from config import config


async def GetmeghalayaAnnoucements():
    try :
        return scapre_website(config["Meghalaya"])
    except Exception as e:
        return f"GetmeghalayaAnnoucements error occurred: {str(e)}"