from app_types.govt_item import GovtItem
from typing import Optional,TypedDict
from datetime import datetime
from service.db.Original_Annoucements import OriginalAnnouncementsDbService
from app_types.OriginalAnnouncement import OriginalAnnouncement

class InsertAnnouncement(TypedDict):
    title : str
    content:str
    link :Optional[str]
    pdf_link :Optional[str]
    

async def insert_annoucements_db(items: list[InsertAnnouncement]):
    try:
        new_items = []

        for item in items:
            existing_announcement = await OriginalAnnouncementsDbService.find_announcement_by_title(item['title'])
            if not existing_announcement:

                annoucement = OriginalAnnouncement(
                    title=item['title'],
                    content=item['content'],
                    state=item['content'],
                    date=datetime.now(),
                    source_link= item.get('link').strip() if item.get('link') else item.get("pdf_link")
                )
                announcement_id = await OriginalAnnouncementsDbService.insert_announcement(annoucement)

                new_items.append({**annoucement, " OriginalAnnouncementid": str(announcement_id)})

                print(f"Inserted announcement with id: {announcement_id}")

        return new_items
    except Exception as e:
        print(f"Error inserting announcement: {e}")
        return None