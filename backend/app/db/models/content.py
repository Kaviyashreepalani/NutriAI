from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class EducationalContent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "educational_content"

    slug = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(JSONB, nullable=False)
    body = Column(JSONB, nullable=False)  # {"en": "...", "ta": "...", ...}
    category = Column(String(64), nullable=False)
    status = Column(Enum("draft", "expert_reviewed", "published", name="content_status_enum"), default="draft", nullable=False)
    translation_review_status = Column(JSONB, default=dict, nullable=False)  # {"ta": "machine_draft", ...}
    references_list = Column(JSONB, default=list, nullable=False)


class ReferenceCatalog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reference_catalog"

    citation = Column(Text, nullable=False)
    url = Column(String(512), nullable=True)
    doi = Column(String(128), nullable=True)
    year = Column(Integer, nullable=True)


class Statistic(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "statistics"

    metric_name = Column(String(255), nullable=False)
    value = Column(Numeric(6, 2), nullable=True)  # Null if pending verification!
    unit = Column(String(32), default="%", nullable=False)
    population_group = Column(String(128), nullable=False)  # e.g., "Adolescent Girls (15-19)", "Women of Reproductive Age (15-49)"
    survey_name = Column(String(128), nullable=False)      # e.g., "NFHS-5", "ICMR-NIN"
    survey_year = Column(String(32), nullable=False)       # e.g., "2019-21"
    definition = Column(Text, nullable=False)
    reference_id = Column(UUID(as_uuid=True), ForeignKey("reference_catalog.id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum("verified", "pending", name="stat_status_enum"), default="pending", nullable=False, index=True)


class Feedback(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "feedback"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    rating = Column(Integer, nullable=False)  # 1 to 5
    comment = Column(Text, nullable=True)


class ContactMessage(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "contact_messages"

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(32), default="received", nullable=False)

