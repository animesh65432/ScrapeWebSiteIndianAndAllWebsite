from config import config
from .utils import scrape_website

async def GetDadraandNagarHaveliDamanDiuAnnoucements():
    try :
        print("Scraping DadraandNagarHaveliDamanDiu Announcements...")
        
        return await scrape_website(config["DadraandNagarHaveliDamanDiu"])
    except Exception as e :
        print("Error GetDadraandNagarHaveliDamanDiuAnnoucements",e)
        return None