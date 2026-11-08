from sqlalchemy import Column, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class ChatSession(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "chat_sessions"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    scope = Column(Enum("general", "personalized", name="chat_scope_enum"), default="general", nullable=False)
    language = Column(String(8), default="en", nullable=False)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at")


class ChatMessage(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "chat_messages"

    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(Enum("user", "assistant", "system", name="chat_role_enum"), nullable=False)
    content = Column(Text, nullable=False)
    grounding = Column(JSONB, default=dict, nullable=False)  # assessment_id, recommendation_id, ingredient_ids, rule_versions
    safety_flags = Column(JSONB, default=dict, nullable=False)  # number_guard_passed, medical_disclaimer_attached
    input_mode = Column(Enum("text", "voice", name="chat_input_mode_enum"), default="text", nullable=False)

    session = relationship("ChatSession", back_populates="messages")

