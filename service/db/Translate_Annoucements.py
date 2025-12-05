from pymongo import AsyncMongoClient
from .ConnectDb import get_client
from app_types.TranslateAnnouncement import TranslateAnnouncement
from bson import ObjectId


class TranslateAnnouncementsDbService:
    _client: AsyncMongoClient = None

    @classmethod
    async def get_collection(cls):
        client = await get_client(cls)
        db = client["Indian_Govt_Announcements"]
        return db["Translated_Announcements"]
    

    @classmethod
    async def insert_translated_announcement(cls, announcement: TranslateAnnouncement):
        collection = await cls.get_collection()

       
        data = announcement.copy()

     
        if isinstance(data["originalAnnouncementId"], str):
            data["originalAnnouncementId"] = ObjectId(data["originalAnnouncementId"])

        result = await collection.insert_one(data)
        return result.inserted_id
    

    @classmethod
    async def check_existing_translation(cls, originalAnnouncementId: str, language: str) -> bool:
        collection = await cls.get_collection()

      
        if isinstance(originalAnnouncementId, str):
            originalAnnouncementId = ObjectId(originalAnnouncementId)

        existing = await collection.find_one({
            "originalAnnouncementId": originalAnnouncementId,
            "language": language
        })

        return existing is not None
