import asyncio
from Scrape import scarpe_westBengal_Annoucements ,scarpe_Assam_Annoucements,scrap_Dehli_Website,scrape_Goa_Annoucements,scapre_HimachalPradesh_Annoucements,scrape_ArunachalPradesh_Annoucements ,ScrapeChhattisgarhAnnoucement ,GetJammuandKashmirAnnoucements,GetjharkhandGovAnnoucements ,GetKarnataka_Govt_Annoucements,GetKeralaGovtAnnoucements,GetAllLadakhAnnoucements ,GetAllMaharashtraAnnoucements,GetAllMadhyaPradeshAnnoucements ,GetAllManipurAnnoucements ,GetmeghalayaAnnoucements,GetMizoramAnnoucements ,GetNagalandAnnoucements,GetOdishaAnnouncements,GetPuducherryAnnoucements,GetPunjabAnnoucements,GetRajasthanAnnoucements ,GetSikkimAnnouncements,GetallTamilNaduAnnoucements ,GetAllTelanganaAnnoucements ,GetAllTripuraAnnoucements ,GetUttarakhandAnnouncements,GetUttarPradeshAnnoucements

async def scrape_all_states():
    # tasks = [
    #     scarpe_westBengal_Annoucements(),
    #     scarpe_Assam_Annoucements(),
    #     scrap_Dehli_Website(),
    #     scrape_Goa_Annoucements(),
    #     scapre_HimachalPradesh_Annoucements()
    # ]

    # results = await asyncio.gather(*tasks, return_exceptions=True)

    # westBengal = results[0] if not isinstance(results[0], Exception) else []
    # assam = results[1] if not isinstance(results[1], Exception) else []
    # delhi = results[2] if not isinstance(results[2], Exception) else []
    # goa = results[3] if not isinstance(results[3], Exception) else []
    # himachal = results[4] if not isinstance(results[4], Exception) else []
    # print(await GetJammuandKashmirAnnoucements())
    print(await GetUttarPradeshAnnoucements())
    return ""


async def main():
    await scrape_all_states()

asyncio.run(main())
