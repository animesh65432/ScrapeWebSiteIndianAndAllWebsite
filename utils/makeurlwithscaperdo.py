import urllib
from config import config

def makeurlwithscaperdo(url:str,part:str,isScraperAPIUsed:bool=True)->str:
    parsed_url = urllib.parse.quote(url,safe="")
    if (part == "north_India" and isScraperAPIUsed) or (part == "northEast_India" and isScraperAPIUsed ==True):
        print("Using North India Scraper API Token")
        url = f"http://api.scrape.do/?token={config['NORTH_SCARPER_AND_NORTHEAST_INDIA_API_TOEKN']}&url={parsed_url}"
    elif (part == "central_India" and isScraperAPIUsed) or (part == "east_India" and isScraperAPIUsed):
        print("Using Central India Scraper API Token")
        url = f"http://api.scrape.do/?token={config['CENTRAL_INDIA_AND_EAST_INDIA_SCARPER_API_TOEKN']}&render=true&url={parsed_url}"
    elif (part == "south_india" and isScraperAPIUsed):
        print("Using South India Scraper API Token",config['SOUTH_INDIA_AND_WEST_INDIA_API_TOKEN'])
        url = f"http://api.scrape.do/?token={config['SOUTH_INDIA_AND_WEST_INDIA_API_TOKEN']}&render=true&url={parsed_url}"
    return url