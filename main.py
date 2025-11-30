import asyncio
from Scrape.westbengal import GetwestBengalAnnoucements
from Scrape.Assam import GetAssamAnnoucements
from Scrape.Dehli import GetDehliAnnoucements
from Scrape.Goa import GetGoaAnnoucements
from Scrape.HimachalPradesh import GetHimachalPradeshAnnoucements
from Scrape.ArunachalPradesh import GetArunachalPradeshAnnoucements
from Scrape.Chandigarh import GetChandigrahAnnoucements
from Scrape.JammuandKashmir import GetJammuandKashmirAnnoucements
from Scrape.jharkhand import GetjharkhandGovAnnoucements
from Scrape.Karnataka import GetKarnatakaGovtAnnoucements
from Scrape.Kerala import GetKeralaGovtAnnoucements
from Scrape.Ladakh import GetAllLadakhAnnoucements
from Scrape.Maharashtra import GetAllMaharashtraAnnoucements
from Scrape.MadhyaPradesh import GetAllMadhyaPradeshAnnoucements
from Scrape.Manipur import GetAllManipurAnnoucements
from Scrape.Meghalaya import GetmeghalayaAnnoucements
from Scrape.Mizoram import GetMizoramAnnoucements
from Scrape.Nagaland import GetNagalandAnnoucements
from Scrape.Odisha import GetOdishaAnnouncements
from Scrape.Puducherry import GetPuducherryAnnoucements
from Scrape.Punjab import GetPunjabAnnoucements
from Scrape.Rajasthan import GetRajasthanAnnoucements
from Scrape.Sikkim import GetSikkimAnnouncements
from Scrape.TamilNadu import GetallTamilNaduAnnoucements
from Scrape.Telangana import GetAllTelanganaAnnoucements
from Scrape.Tripura import GetAllTripuraAnnoucements
from Scrape.Uttarakhand import GetUttarakhandAnnouncements
from Scrape.UttarPradesh import GetUttarPradeshAnnoucements
from Scrape.Gujarat import GetGujaratAnnoucements
from Scrape.Haryana import GetHaryanaAnnoucements
from Scrape.Lakshadweep import GetLaskhadweepAnnoucements
from Scrape.Chandigarh import GetChandigrahAnnoucements
from Scrape.DadraandNagarHaveliDamanDiu import GetDadraandNagarHaveliDamanDiuAnnoucements
from Scrape.AndamanNicobarIslands import GetAndamanNicobarIslandsAnnoucements
from Scrape.Bihar import GetBiharAnnoucements
from Scrape.Andhrapradesh import GetAndhrapradeshAnnoucements

async def scrape_all_states():
    try:
        tasks = [
            GetwestBengalAnnoucements(),
            GetAssamAnnoucements(),
            GetDehliAnnoucements(),
            GetGoaAnnoucements(),
            GetHimachalPradeshAnnoucements(),
            GetArunachalPradeshAnnoucements(),
            GetChandigrahAnnoucements(),
            GetJammuandKashmirAnnoucements(),
            GetjharkhandGovAnnoucements(),
            GetKarnatakaGovtAnnoucements(),
            GetKeralaGovtAnnoucements(),
            GetAllLadakhAnnoucements(),
            GetAllMaharashtraAnnoucements(),
            GetAllMadhyaPradeshAnnoucements(),
            GetAllManipurAnnoucements(),
            GetmeghalayaAnnoucements(),
            GetMizoramAnnoucements(),
            GetNagalandAnnoucements(),
            GetOdishaAnnouncements(),
            GetPuducherryAnnoucements(),
            GetPunjabAnnoucements(),
            GetRajasthanAnnoucements(),
            GetSikkimAnnouncements(),
            GetallTamilNaduAnnoucements(),
            GetAllTelanganaAnnoucements(),
            GetAllTripuraAnnoucements(),
            GetUttarakhandAnnouncements(),
            GetUttarPradeshAnnoucements(),
            GetGujaratAnnoucements(),
            GetHaryanaAnnoucements(),
            GetLaskhadweepAnnoucements(),
            GetChandigrahAnnoucements(),
            GetDadraandNagarHaveliDamanDiuAnnoucements(),
            GetAndamanNicobarIslandsAnnoucements(),
            GetBiharAnnoucements(),
            GetAndhrapradeshAnnoucements()
        ]
        
        results = await asyncio.gather(*tasks)

        return "All states scraped successfully"
    except Exception as e:
        print("Error in scrape_all_states", e)
        return None
   


async def main():
    try:
        print("Starting to scrape all states...")
        res = await scrape_all_states()
        print(res)
    except Exception as e:
        print("Error in main", e)

asyncio.run(main())
