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
        # print(res)

        res = await scan_pdf_url("https://nagaland.gov.in/storage/PostFiles/Procedures%20And%20Guidelines%20For%20Lien%20On%20Post%20And%20Technical%20Resignation.pdf")
        print("Converted Markdown:", res)

        # res = await pdf_url_to_markdown("https://assam.gov.in/sites/default/files/2024-10/1.%20NOTICE%20REG.%20DOWNLOADING%20OF%20OMR%20ANSWER%20SHEET_0.pdf")
        # print("Nagaland Assam Converted Markdown:", res) 
        
        # if res:
        #     print("PDF to Markdown conversion successful.",res)
        # else:
        #     print("PDF to Markdown conversion failed.")

        return "Test completed."
    except Exception as e:
        print(f"Error during: {e}")

if __name__ == "__main__":
    asyncio.run(test())
