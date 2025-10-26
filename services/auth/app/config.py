from dotenv import load_dotenv
import os


load_dotenv()

class Config:
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    DATABASE_URI = os.environ["DATABASE_URI"]
    PORT = int(os.environ["PORT"])
    DEPUG = os.environ['DEPUG'] == "True"
