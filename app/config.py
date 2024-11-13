import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file if available

class Config:
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
