from fastapi import APIRouter,Request
from app.models.chat import ChatRequest, ChatResponse
from app.services.chatbot import chat
from pydantic import BaseModel
from typing import List, Any
import requests
import os

VERIFY_TOKEN = "verifyToken@12345@"
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")  # WhatsApp Cloud API permanent access token
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")  # Your business phone number ID from Meta

router = APIRouter()

class HistoryItem(BaseModel):
    content: str
    role: str

class ChatRequest(BaseModel):
    message: str
    history: List[HistoryItem] = []

@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    history = [item.dict() for item in request.history]
    return {"reply": chat(request.message, history)}

@router.get("/webhook")
async def verify_webhook(request: Request):
    """
    This endpoint is called by Meta during WhatsApp webhook verification.
    It must return the 'hub.challenge' if the verify token matches.
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return {"error": "Verification failed"}

@router.post("/webhook")
async def receive_whatsapp_message(request: Request):
    """
    Receives WhatsApp messages from Meta and replies using the chat() function.
    """
    data = await request.json()
    print("Incoming data:", data)
    try:
        # Extract the incoming message
        entry = data["entry"][0]["changes"][0]["value"]
        messages = entry.get("messages", [])

        if messages:
            from_number = messages[0]["from"]  # Customer's WhatsApp number
            msg_body = messages[0]["text"]["body"]  # Message text

            print("from_number:", from_number)

            print("msg_body:", msg_body)

            # Call your chatbot function
            reply_text = chat(msg_body, history=[])

            print("reply_text:", reply_text)

            # Send reply to WhatsApp using Graph API
            url = f"https://graph.facebook.com/v16.0/{PHONE_NUMBER_ID}/messages"
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": from_number,
                "text": {"body": reply_text}
            }
            resp = requests.post(url, json=payload, headers=headers)
            print("Graph API response:", resp.status_code, resp.text)

    except Exception as e:
        print("Error processing message:", e)

    return {"status": "ok"}
