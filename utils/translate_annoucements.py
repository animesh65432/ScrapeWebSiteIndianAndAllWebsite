from app_types.TranslateAnnouncement import TranslateAnnouncement
from .translate_announcement_english import translate_announcement_english
from utils.translate_announcement_indianlan import translate_announcement_indianLanguages
from utils.languages import INDIAN_LANGUAGES
from typing import TypedDict
from datetime import date
import asyncio


class Announcement(TypedDict):
    title: str
    content: str
    source_link: str
    date: date
    state: str
    announcementId: str


async def translate_announcements(
    announcements: list[Announcement]
) -> list[TranslateAnnouncement]:

    semaphore = asyncio.Semaphore(1)  

    async def process_announcement(announcement: Announcement):
        async with semaphore:
            print(f"🔄 Translating to English: {announcement['title']}")

            # 1️⃣ English translation
            english_result = await translate_announcement_english(
                announcement,
                "en"
            )

            if not english_result["success"]:
                return [english_result]

            english_data = english_result["data"]

            # ✅ INSERT ENGLISH
            all_results = [english_data]

            print(f"✅ English inserted: {english_data['title']}")

            # 2️⃣ Indian languages
            for lang in INDIAN_LANGUAGES:
                print(f"🌐 Translating → {lang}: {english_data['title']}")

                result = await translate_announcement_indianLanguages(
                    english_data,
                    lang
                )

                if result["success"]:
                    all_results.append(result["data"])

            return all_results

    tasks = [process_announcement(a) for a in announcements]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successful = []
    failed = []

    for r in results:
        if isinstance(r, Exception):
            failed.append({"error": str(r)})
        else:
            successful.extend(r)

    print(
        f"✅ Total saved translations: {len(successful)} | "
        f"❌ Failed batches: {len(failed)}"
    )

    return successful
