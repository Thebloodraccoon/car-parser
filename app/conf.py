import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fake_useragent import UserAgent
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB: str = os.getenv("MONGODB_DB", "car_listings")

# Database client instance
client = AsyncIOMotorClient(MONGODB_URL)
database = client[MONGODB_DB]

# Collections
CAR_COLLECTION: str = "cars"
USER_COLLECTION: str = "users"

# PROXY SERVER
PROXY: str | None = os.getenv("PROXY")

# FAKE AGENT
ua = UserAgent()

# JWT settings
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")


# Redis settings
HOST_REDIS: str = os.getenv("HOST_REDIS", "redis")
PORT_REDIS: str = os.getenv("PORT_REDIS", "6379")
DB_REDIS: str = os.getenv("DB_REDIS", "0")


@asynccontextmanager
async def get_redis():
    redis_client = Redis(
        host=HOST_REDIS,
        port=int(PORT_REDIS),
        db=DB_REDIS,
        decode_responses=True,
    )
    try:
        yield redis_client
    finally:
        await redis_client.aclose()


# Default user
DEFAULT_USER_NAME: str = os.getenv("DEFAULT_USER_NAME", "admin")
DEFAULT_USER_EMAIL: str = os.getenv("DEFAULT_USER_EMAIL", "admin@admin.com")
DEFAULT_USER_PASSWORD = os.getenv("DEFAULT_USER_PASSWORD", "admin_password")
