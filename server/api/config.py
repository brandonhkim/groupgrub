import os
import redis
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url(os.environ.get("REDIS_URL"))
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
