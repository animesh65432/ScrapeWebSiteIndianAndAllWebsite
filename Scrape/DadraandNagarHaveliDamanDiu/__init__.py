from config import config
from .utils import scrape_website

async def GetDadraandNagarHaveliDamanDiuAnnoucements():
    try :
        return scrape_website(config["DadraandNagarHaveliDamanDiu"])
    except Exception as e :
        print("GetDadraandNagarHaveliDamanDiuAnnoucements",e)
        return None