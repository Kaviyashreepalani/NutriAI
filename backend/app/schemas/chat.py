import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatSessionCreate(BaseModel):
    scope: str = Field(default="general", pattern="^(general|personalized)$")
    language: str = Field(default="en", pattern="^(en|ta|hi|te|ml)$")


class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
    input_mode: str = Field(default="text", pattern="^(text|voice)$")


class ChatMessageResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    role: str
    content: str
    grounding: Dict[str, Any] = Field(default_factory=dict)
    safety_flags: Dict[str, Any] = Field(default_factory=dict)
    input_mode: str
    created_at: datetime


class ChatSessionResponse(BaseModel):
    id: uuid.UUID
    scope: str
    language: str
    messages: List[ChatMessageResponse] = Field(default_factory=list)
    created_at: datetime


class STTResponse(BaseModel):
    transcript: str
    language: str
    confidence: float = 0.95


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)
    language: str = Field(default="en-IN")

