from pymongo import AsyncMongoClient
from .ConnectDb import get_client
from app_types.TranslateAnnouncement import TranslateAnnouncement

class TranslateAnnouncementsDbService:
    _client: AsyncMongoClient = None

    @classmethod
    async def get_collection(cls):
        client = await get_client(cls)
        db = client["Indian_Govt_Announcements"]
        collection = db["Translated_Announcements"]
        return collection
    
    @classmethod
    async def insert_translated_announcement(cls, announcement:TranslateAnnouncement):
        collection = await cls.get_collection()
        result = await collection.insert_one(announcement)
        return result.inserted_id
    
    