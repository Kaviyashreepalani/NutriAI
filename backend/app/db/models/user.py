from datetime import date
from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin, SoftDeleteMixin


class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    auth_uid = Column(String(128), unique=True, nullable=False, index=True)
    auth_provider = Column(String(32), default="supabase", nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    email_verified = Column(Boolean, default=False, nullable=False)
    role = Column(
        Enum("user", "admin", "nutritionist", name="user_role_enum"),
        default="user",
        nullable=False,
    )
    preferred_language = Column(
        Enum("en", "ta", "hi", "te", "ml", name="preferred_language_enum"),
        default="en",
        nullable=False,
    )
    date_of_birth = Column(Date, nullable=False)
    status = Column(String(32), default="active", nullable=False)
    guardian_consent_id = Column(UUID(as_uuid=True), nullable=True)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    consents = relationship("Consent", back_populates="user", cascade="all, delete-orphan")
    measurements = relationship("PhysicalMeasurement", back_populates="user", cascade="all, delete-orphan")
    dietary_preferences = relationship("DietaryPreference", back_populates="user", cascade="all, delete-orphan")
    allergies = relationship("Allergy", back_populates="user", cascade="all, delete-orphan")
    health_info = relationship("HealthInformation", back_populates="user", uselist=False, cascade="all, delete-orphan")
    reports = relationship("UploadedReport", back_populates="user", cascade="all, delete-orphan")
    assessments = relationship("NutritionalAssessment", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("GeneratedRecommendation", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    consumption_plans = relationship("ConsumptionPlan", back_populates="user", cascade="all, delete-orphan")

    @property
    def age(self) -> int:
        """Dynamically compute age from date of birth. Age is never stored in DB."""
        if not self.date_of_birth:
            return 0
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )


class UserProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "user_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    sex = Column(String(16), default="female", nullable=False)
    phone = Column(String(32), nullable=True)
    address_line = Column(Text, nullable=True)
    city = Column(String(128), nullable=True)
    state = Column(String(128), nullable=True)
    pin_code = Column(String(6), nullable=True)  # Regex ^[1-9][0-9]{5}$
    profile_completion_pct = Column(Integer, default=20, nullable=False)

    user = relationship("User", back_populates="profile")

