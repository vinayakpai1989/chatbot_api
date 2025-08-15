from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.chatbot import chat
from pydantic import BaseModel
from typing import List, Any


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
