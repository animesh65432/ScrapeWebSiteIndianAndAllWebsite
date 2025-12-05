from app_types.TranslateAnnouncement import TranslateAnnouncement
from .translate_announcement import translate_announcement
from typing import TypedDict
from datetime import date
from data import languages
import asyncio
from collections import deque
import time

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

    print(await translate_announcement(announcements[0], languages[1]))
    return all_translations
