from .utils import scapre_website
from config import config


async def GetOdishaAnnouncements():
    return scapre_website(config["Odisha"])