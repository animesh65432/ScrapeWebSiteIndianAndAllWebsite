import asyncio
from utils.pdf_url_to_markdown import pdf_url_to_markdown
from utils.OcrScanpdfurl import scan_pdf_url
from Scrape.Chandigarh import GetChandigrahAnnoucements
from Scrape.JammuandKashmir import GetJammuandKashmirAnnoucements
from Scrape.jharkhand import GetjharkhandGovAnnoucements
from Scrape.Karnataka import GetKarnatakaGovtAnnoucements
from Scrape.Ladakh import GetAllLadakhAnnoucements
from Scrape.Meghalaya import GetmeghalayaAnnoucements
from Scrape.Nagaland import GetNagalandAnnoucements
from Scrape.Odisha import GetOdishaAnnouncements
from Scrape.Punjab import GetPunjabAnnoucements
from Scrape.TamilNadu import GetallTamilNaduAnnoucements
from Scrape.Tripura import GetAllTripuraAnnoucements
from Scrape.Uttarakhand import GetUttarakhandAnnouncements
from Scrape.UttarPradesh import GetUttarPradeshAnnoucements
from Scrape.AndamanNicobarIslands import GetAndamanNicobarIslandsAnnoucements
from Scrape.Bihar import GetBiharAnnoucements
from Scrape.Dehli import GetDehliAnnoucements
from Scrape.Goa import GetGoaAnnoucements
from Scrape.Gujarat import GetGujaratAnnoucements
from Scrape.HimachalPradesh import GetHimachalPradeshAnnoucements
from Scrape.IndianGovtAnnoucement import GetAllIndianGovtAnnouncements
from Scrape.Kerala import GetKeralaGovtAnnoucements
from Scrape.MadhyaPradesh import GetAllMadhyaPradeshAnnoucements
from Scrape.Maharashtra import GetAllMaharashtraAnnoucements
from Scrape.Mizoram import GetMizoramAnnoucements
from Scrape.Rajasthan import GetRajasthanAnnoucements
from Scrape.Mizoram import GetMizoramAnnoucements

async def test():
    try:
        # res =  await GetAssamAnnoucements()
        # res =  await GetChandigrahAnnoucements()
        # res = await GetJammuandKashmirAnnoucements()
        # res = await GetjharkhandGovAnnoucements()
        # res = await GetKarnatakaGovtAnnoucements()
        # res = await GetAllLadakhAnnoucements()
        # res = await GetmeghalayaAnnoucements()
        # res = await GetNagalandAnnoucements()
        # res = await GetOdishaAnnouncements()
        # res = await GetPunjabAnnoucements()
        # res = await GetallTamilNaduAnnoucements()
        # res = await GetAllTripuraAnnoucements()
        # res = await GetAndamanNicobarIslandsAnnoucements()
        # res = await GetBiharAnnoucements()
        # res = await GetGujaratAnnoucements()
        # res = await GetGoaAnnoucements()
        res = await GetMizoramAnnoucements()
        print("Announcements:", res)

        # res = await scan_pdf_url("https://cms.tn.gov.in/cms_migrated/document/press_release/pr301125_2875.pdf")
        # print("Converted Markdown:", res)

        
        # if res:
        #     print("PDF to Markdown conversion successful.",res)
        # else:
        #     print("PDF to Markdown conversion failed.")

        return "Test completed."
    except Exception as e:
        print(f"Error during: {e}")

if __name__ == "__main__":
    asyncio.run(test())
