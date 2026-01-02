from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any
from dotenv import load_dotenv
import os

load_dotenv() 

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASSWORD")

MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"

client = AsyncIOMotorClient(MONGO_URL)
mongo_db = client["items"]



