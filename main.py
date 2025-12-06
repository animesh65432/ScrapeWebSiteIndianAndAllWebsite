import asyncio
from utils.scrape_all_states import scrape_all_states
from utils.classify_announcement_or_news import classify_announcement_or_news
from utils.scrapthepdfcontent import extract_text_from_pdf_bytes
from utils.insert_annoucements_db import insert_annoucements_db
from service.Faiss import FaissService
from utils.translate_annoucements import translate_announcements
from utils.insert_translate_annoucements import insert_translate_announcements
from data import data
from service.db.Original_Annoucements import OriginalAnnouncementsDbService
from utils.format_announcement import format_announcement
from Scrape.Ladakh import GetAllLadakhAnnoucements
from Scrape.Maharashtra import GetAllMaharashtraAnnoucements
from utils.cleanup_chrome_processes import cleanup_chrome_processes

async def main():
    try:
        await cleanup_chrome_processes()
        await asyncio.sleep(2)
        announcements = await scrape_all_states(batch_size=1)
        print("scraped announcements from all states",len(announcements))
        if not announcements or len(announcements) == 0:
            print("No announcements scraped. Exiting.")
            return None
        faiss_service = FaissService(announcements)
        unique_announcements = faiss_service.get_unique(threshold=0.90)
        print("unique announcements after faiss",len(unique_announcements))
        classified_announcements = await classify_announcement_or_news(unique_announcements)
        print("classified announcements",classified_announcements)
        announcements_with_pdf_text = await extract_text_from_pdf_bytes(classified_announcements)
        print("announcements with pdf text extracted",announcements_with_pdf_text)
        await insert_annoucements_db(announcements_with_pdf_text)


        # print(await GetAllLadakhAnnoucements())

        # db = OriginalAnnouncementsDbService()
        
        # docs = await db.find_announcements()


        # translateAnnouncements = await translate_announcements([{
        #     'title': docs[0]['title'],
        #     'content': docs[0]['content'],
        #     'state': docs[0]['state'],
        #     'pdf_text': docs[0]['source_link'],
        #     id :str(docs[0]['_id'])
        # }])

        # print(translateAnnouncements)

        
        # await insert_translate_announcements(translateAnnouncements)


        print("✅ All tasks completed successfully!")

        return []

    except Exception as e:
        print(f"❌ Critical error in main: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())
