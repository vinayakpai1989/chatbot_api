import requests
from app.core.config import settings

def push(message: str):
    payload = {
        "user": settings.PUSHOVER_USER,
        "token": settings.PUSHOVER_TOKEN,
        "message": message
    }
    requests.post(settings.PUSHOVER_URL, data=payload)
