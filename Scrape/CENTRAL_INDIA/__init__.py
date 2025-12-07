from .Chhattisgarh import GetChhattisgarhAnnoucement
from .MadhyaPradesh import GetAllMadhyaPradeshAnnoucements
from utils.save_to_json import save_to_json


async def GetAllCentralIndiaAnnoucements():
    try:
        MadhyaPradeshAnnoucements = await GetAllMadhyaPradeshAnnoucements()
        ChhattisgarhAnnoucements = await GetChhattisgarhAnnoucement()
        all_annoucements = MadhyaPradeshAnnoucements + ChhattisgarhAnnoucements
        print(f"Total Central India Announcements: {len(all_annoucements)}")
        save_to_json(all_annoucements, "central")

        return all_annoucements
    except Exception as e:
        print(f"Error in GetAllCentralIndiaAnnoucements: {e}")
        return []