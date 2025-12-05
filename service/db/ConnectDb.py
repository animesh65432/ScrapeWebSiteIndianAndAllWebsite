from pymongo import AsyncMongoClient
from config import config

async def get_client(cls) -> AsyncMongoClient:
    if cls._client is None:
        cls._client = AsyncMongoClient(config["MONGODB_URI"])
    return cls._client
