from Scrape.IndianGovtAnnoucement import GetAllIndianGovtAnnouncements
import asyncio

async def test():
    try:
        res = await GetAllIndianGovtAnnouncements()
        print("Function executed successfully.",res)
    except Exception as e:
        print(f"Error during: {e}")

if __name__ == "__main__":
    asyncio.run(test())
