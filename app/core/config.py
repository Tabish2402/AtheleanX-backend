import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Application")
    ENV: str = os.getenv("ENV", "development")

settings = Settings()