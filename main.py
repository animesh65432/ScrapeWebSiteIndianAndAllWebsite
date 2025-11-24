import asyncio
from westbengal import scarpe_westBengal_Annoucements

async def scrape_all_website():
    try:
        WestBengalAnnoucements = await scarpe_westBengal_Annoucements()
        print(WestBengalAnnoucements)
    except :
        print("scarpin error happend")


async def main():
    await scrape_all_website()

asyncio.run(main())
