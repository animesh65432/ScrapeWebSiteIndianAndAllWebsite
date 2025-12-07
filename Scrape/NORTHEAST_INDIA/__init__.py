from .ArunachalPradesh import GetArunachalPradeshAnnoucements
from .Assam import GetAssamAnnoucements
from .Manipur import GetAllManipurAnnoucements
from .Meghalaya import GetmeghalayaAnnoucements
from .Mizoram import GetMizoramAnnoucements
from .Nagaland import GetNagalandAnnoucements
from .Sikkim import GetSikkimAnnouncements
from .Tripura import GetAllTripuraAnnoucements

async def GetNORTHEASTINDIAAnnoucements():
    announcements = []
    try:
        announcements += await GetArunachalPradeshAnnoucements()
        announcements += await GetAssamAnnoucements()
        announcements += await GetAllManipurAnnoucements()
        announcements += await GetmeghalayaAnnoucements()
        announcements += await GetMizoramAnnoucements()
        announcements += await GetNagalandAnnoucements()
        announcements += await GetSikkimAnnouncements()
        announcements += await GetAllTripuraAnnoucements()
        return announcements
    except Exception as e:
        print("Error in GetNORTHEASTINDIAAnnoucements", e)
        return announcements