from dotenv import load_dotenv
import os


load_dotenv()

class Config:
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    DATABASE_URI = os.environ["DATABASE_URI"]
    REDIS_URL = os.environ["REDIS_URL"]
    ALLOWED_API_TOKENS = os.environ["ALLOWED_API_TOKENS"].split(",")
    DEPUG = os.environ["DEPUG"] == "True"
    PORT = int(os.environ["PORT"])