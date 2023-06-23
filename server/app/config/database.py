from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

# from iam.models import User, AccessToken
from api.consumable.models import Consumable
from config.settings import settings


async def initiate_database():
    client = AsyncIOMotorClient(settings.DATABASE_URI)
    await init_beanie(database=client.get_database(), document_models=[Consumable])
