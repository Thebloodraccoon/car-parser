import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from fake_useragent import UserAgent


# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "car_listings")

# Database client instance
client = AsyncIOMotorClient(MONGODB_URL)
database = client[MONGODB_DB]

# Collections
CAR_COLLECTION = "cars"
USER_COLLECTION = "users"

# Redis clients
HOST_REDIS = os.getenv(
    "HOST_REDIS",
)
PORT_REDIS = os.getenv("PORT_REDIS")
DB_REDIS = os.getenv("DB_REDIS")


@asynccontextmanager
async def get_redis():
    redis_client = Redis(
        host=HOST_REDIS,
        port=PORT_REDIS,
        db=DB_REDIS,
        decode_responses=True,
    )
    try:
        yield redis_client
    finally:
        await redis_client.aclose()


# PROXY SERVER
PROXY = os.getenv("PROXY")

# FAKE AGENT
ua = UserAgent()


# JWT SETTINGS
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")


# Default admin credentials
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_EMAIL = "admin@admin.com"
DEFAULT_ADMIN_PASSWORD = "admin_strong_password"
