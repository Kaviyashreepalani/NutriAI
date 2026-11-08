from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin
from app.core.encryption import encryptor


class HealthInformation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "health_information"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    recorded_on = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    known_deficiencies = Column(ARRAY(String), default=list, nullable=False)
    pregnancy_status = Column(String(32), default="not_pregnant", nullable=False)  # not_pregnant, pregnant_trimester_1, pregnant_trimester_2, pregnant_trimester_3, lactating

    # Encrypted fields (AES-256-GCM base64 payload)
    diagnoses_encrypted = Column(Text, nullable=True)
    menstrual_info_encrypted = Column(Text, nullable=True)
    supplements_encrypted = Column(Text, nullable=True)
    medications_encrypted = Column(Text, nullable=True)
    notes_encrypted = Column(Text, nullable=True)

    user = relationship("User", back_populates="health_info")

    # Helper getters/setters with column encryption
    @property
    def diagnoses(self) -> str:
        return encryptor.decrypt(self.diagnoses_encrypted or "")

    @diagnoses.setter
    def diagnoses(self, val: str):
        self.diagnoses_encrypted = encryptor.encrypt(val)

    @property
    def menstrual_info(self) -> dict:
        return encryptor.decrypt_json(self.menstrual_info_encrypted or "") or {}

    @menstrual_info.setter
    def menstrual_info(self, val: dict):
        self.menstrual_info_encrypted = encryptor.encrypt_json(val)

    @property
    def supplements(self) -> list:
        return encryptor.decrypt_json(self.supplements_encrypted or "") or []

    @supplements.setter
    def supplements(self, val: list):
        self.supplements_encrypted = encryptor.encrypt_json(val)

    @property
    def medications(self) -> list:
        return encryptor.decrypt_json(self.medications_encrypted or "") or []

    @medications.setter
    def medications(self, val: list):
        self.medications_encrypted = encryptor.encrypt_json(val)

    @property
    def notes(self) -> str:
        return encryptor.decrypt(self.notes_encrypted or "")

    @notes.setter
    def notes(self, val: str):
        self.notes_encrypted = encryptor.encrypt(val)

