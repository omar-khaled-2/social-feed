from dotenv import load_dotenv
import os


load_dotenv()

class Config:
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    DATABASE_URI = os.environ["DATABASE_URI"]
    POST_IMAGES_BUCKET = os.environ["POST_IMAGES_BUCKET"]
    MINIO_ENDPOINT = os.environ["MINIO_ENDPOINT"]
    MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
    MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]
    AMQP_URI = os.environ["AMQP_URI"]
    CREATED_POSTS_QUEUE_NAME = os.environ["CREATED_POSTS_QUEUE_NAME"]