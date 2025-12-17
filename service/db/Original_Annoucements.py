from pymongo import AsyncMongoClient
from .ConnectDb import get_client
from app_types.OriginalAnnouncement import OriginalAnnouncement
from bson import ObjectId


class OriginalAnnouncementsDbService:
    _client: AsyncMongoClient = None

    @classmethod
    async def get_collection(cls):
        client = await get_client(cls)
        db = client["Indian_Govt_Announcements"]
        collection = db["Original_Announcements"]
        return collection
    
    @classmethod
    async def insert_announcement(cls, announcement: OriginalAnnouncement):
        collection = await cls.get_collection()
        result = await collection.insert_one(announcement)
        return result.inserted_id
    
    @classmethod
    async def find_announcement_by_title(cls, title: str):
        collection = await cls.get_collection()
        announcement = await collection.find_one({"title": title})
        return announcement
    
    @classmethod
    async def find_announcements(cls):
        collection = await cls.get_collection()
        cursor = collection.find({})
        announcements = []
        async for document in cursor:
            announcements.append(document)
        return announcements
    
    @classmethod
    async def find_announcement_by_id(cls, announcement_id):
        collection = await cls.get_collection()
        announcement = await collection.find_one({"_id": ObjectId(announcement_id)})
        return announcement
    

