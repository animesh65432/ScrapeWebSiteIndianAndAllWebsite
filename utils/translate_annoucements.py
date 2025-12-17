from app_types.TranslateAnnouncement import TranslateAnnouncement
from .translate_announcement import translate_announcement
from typing import TypedDict
from datetime import date
from utils.languages import LanGuaGes as languages
import asyncio

class Announcement(TypedDict):
    title:str
    content:str
    source_link:str
    date:date
    state:str
    originalAnnouncementId:str

async def translate_announcements(
    announcements: list[Announcement]
) -> list[TranslateAnnouncement]:
    MAX_CONCURRENT = 1
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async def translate_with_semaphore(announcement: Announcement, lang: str):
        async with semaphore:
            print(f"🔄 Translating to {lang}: {announcement['title'][:30]}...")
            return await translate_announcement(announcement, lang)

    tasks = [
        translate_with_semaphore(announcement, lang)
        for announcement in announcements
        for lang in languages
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    successful_translations = []
    failed_translations = []

    for r in results:
        if isinstance(r, Exception):
            failed_translations.append({
                "success": False,
                "error": str(r)
            })
        elif r["success"] is True:
            successful_translations.append(r["data"])
        else:
            failed_translations.append(r)

    print(
        f"✅ Success: {len(successful_translations)} | "
        f"❌ Failed: {len(failed_translations)}"
    )

    return successful_translations
