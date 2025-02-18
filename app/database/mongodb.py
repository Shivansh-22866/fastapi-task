from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def get_database():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    try:
        yield client[settings.DATABASE_NAME]
    finally:
        client.close()