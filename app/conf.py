import os

from dotenv import load_dotenv
from fake_useragent import UserAgent
from motor.motor_asyncio import AsyncIOMotorClient

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

# PROXY SERVER
PROXY = os.getenv("PROXY")

# FAKE AGENT
ua = UserAgent()


