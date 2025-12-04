from app_types.TranslateAnnouncement import TranslateAnnouncement
from .translate_announcement import translate_announcement
from typing import TypedDict
from datetime import date

class Announcement(TypedDict):
    title:str
    content:str
    source_link:str
    date:date
    state:str
    originalAnnouncementId:str
    

async def translate_announcements(announcement: list[Announcement], target_language: str) ->list[TranslateAnnouncement]:
    try :

        translate_announcements = []

        for ann in announcement:
            translated = await translate_announcement(ann, target_language)
            return [translated]

        return []
    
    except Exception as e:
        print(f"❌ Error in translate_announcements: {e}")
        return []