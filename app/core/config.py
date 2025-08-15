from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Settings:
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    PUSHOVER_USER = os.getenv("PUSHOVER_USER")
    PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
    PUSHOVER_URL = os.getenv("PUSHOVER_URL")
    DEEPSEEK_BASEURL = os.getenv("DEEPSEEK_BASE_URL")

settings = Settings()
