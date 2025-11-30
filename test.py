from Scrape.Andhrapradesh import GetAndhrapradeshAnnoucements
import asyncio

async def test():
    try:
        res = await GetAndhrapradeshAnnoucements()
        print("Function executed successfully.",res)
    except Exception as e:
        print(f"Error during: {e}")

if __name__ == "__main__":
    asyncio.run(test())
