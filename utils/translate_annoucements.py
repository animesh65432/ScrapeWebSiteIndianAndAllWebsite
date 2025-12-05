from app_types.TranslateAnnouncement import TranslateAnnouncement
from .translate_announcement import translate_announcement
from typing import TypedDict
from datetime import date
from data import languages
import asyncio
from collections import deque

class Announcement(TypedDict):
    title:str
    content:str
    source_link:str
    date:date
    state:str
    originalAnnouncementId:str

async def translate_announcements(announcements: list[Announcement]) -> list[TranslateAnnouncement]:
    pending_queue = deque()
    all_translations = []
    
    for announcement in announcements:
        for lang in languages:
            pending_queue.append((announcement, lang))
    
    BATCH_SIZE = 3
    batch_count = 0
    
    while pending_queue:
        batch = []
        
        # Collect 3 items
        for _ in range(min(BATCH_SIZE, len(pending_queue))):
            batch.append(pending_queue.popleft())
        
        # Process sequentially within batch
        for announcement, lang in batch:
            result = await translate_announcement(announcement, lang)
            if result:
                all_translations.append(result)
        
        batch_count += 1
        print(f"✅ Completed batch {batch_count}. Remaining: {len(pending_queue)}")
        
        if pending_queue:
            await asyncio.sleep(0.5)
    
    return all_translations