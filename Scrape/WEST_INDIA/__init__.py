from .Goa import GetGoaAnnoucements
from .Gujarat import GetGujaratAnnoucements
from .Maharashtra import GetAllMaharashtraAnnoucements
from .Rajasthan import GetRajasthanAnnoucements
from  utils.save_to_json import save_to_json

async def GetWESTINDIAAnnoucements():
    try :
        print("Scraping WEST INDIA Announcements...")
        goa_announcements = await GetGoaAnnoucements()
        gujarat_announcements = await GetGujaratAnnoucements()
        maharashtra_announcements = await GetAllMaharashtraAnnoucements()
        rajasthan_announcements = await GetRajasthanAnnoucements()
        all_west_india_announcements = (goa_announcements +
                                        gujarat_announcements +
                                        maharashtra_announcements +
                                        rajasthan_announcements)

        save_to_json(all_west_india_announcements, "west_india")
        
        return all_west_india_announcements
    except Exception as e :
        print("Error in GetWESTINDIAAnnoucements",e)
        return []