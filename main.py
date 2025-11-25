import asyncio
from Scrape import scarpe_westBengal_Annoucements ,scarpe_Assam_Annoucements,scrap_Dehli_Website,scrape_Goa_Annoucements,scapre_HimachalPradesh_Annoucements

async def scrape_all_website():
    try:
        # WestBengalAnnoucements = await scarpe_westBengal_Annoucements()
        # AssamAnnoucements = await scarpe_Assam_Annoucements()
        # DehliAnnoucements = await scrap_Dehli_Website()
        # GoaAnnoucements = await scrape_Goa_Annoucements()
        HimachalPradesh_Annoucements = await scapre_HimachalPradesh_Annoucements()
        print(HimachalPradesh_Annoucements)
        return ""
    except Exception as e :
        print("scarpin error happend",e)


async def main():
    await scrape_all_website()

asyncio.run(main())
