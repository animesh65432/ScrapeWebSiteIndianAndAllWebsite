from Scrape.Odisha import GetOdishaAnnouncements
import asyncio

async def test():
    try:
        res = await GetOdishaAnnouncements()
        print("Function executed successfully.",res)
    except Exception as e:
        print(f"Error during: {e}")

if __name__ == "__main__":
    asyncio.run(GetOdishaAnnouncements())
