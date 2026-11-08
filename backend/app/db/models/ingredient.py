from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class Ingredient(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "ingredients"

    name = Column(String(255), nullable=False, index=True)
    local_names = Column(JSONB, default=dict, nullable=False)  # {"hi": "रागी", "ta": "கேழ்வரகு", "te": "రాగి", "ml": "കൂവരക്"}
    category = Column(String(64), nullable=False, index=True)  # cereal_millet, pulse_legume, oilseed_nut, leafy_green, fruit_veggie, dairy, sweetener_spice
    diet_class = Column(String(32), default="vegan", nullable=False)  # vegan, vegetarian, eggetarian, non_vegetarian
    allergens = Column(ARRAY(String), default=list, nullable=False)  # ["peanut", "tree_nut", "dairy", "gluten", "sesame", "soy"]
    cost_per_kg_inr = Column(Numeric(10, 2), nullable=False)
    cost_as_of = Column(Date, nullable=False)
    availability = Column(String(32), default="high", nullable=False)  # high, seasonal, medium
    processing_notes = Column(Text, nullable=True)
    bioavailability_notes = Column(Text, nullable=True)
    shelf_life_notes = Column(Text, nullable=True)
    min_inclusion_pct = Column(Numeric(5, 2), default=0.0, nullable=False)
    max_inclusion_pct = Column(Numeric(5, 2), default=100.0, nullable=False)
    data_status = Column(Enum("draft", "verified", name="data_status_enum"), default="draft", nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)

    nutrients = relationship("IngredientNutrient", back_populates="ingredient", cascade="all, delete-orphan")


class IngredientNutrient(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "ingredient_nutrients"
    __table_args__ = (
        UniqueConstraint("ingredient_id", "nutrient_code", "source", name="uq_ingredient_nutrient_source"),
    )

    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False, index=True)
    nutrient_code = Column(String(32), nullable=False, index=True)  # energy, protein, iron, folate, b12, vit_c, calcium, fat, added_sugar, sodium, fibre, phytate_flag
    amount_per_100g = Column(Numeric(10, 4), nullable=False)
    unit = Column(String(32), nullable=False)
    source = Column(
        Enum("IFCT_2017", "ICMR_NIN", "USDA", "label", "other", "PLACEHOLDER_DEMO", name="nutrient_source_enum"),
        default="PLACEHOLDER_DEMO",
        nullable=False,
    )
    source_ref = Column(String(255), nullable=True)
    is_heme_iron = Column(Boolean, default=False, nullable=False)
    verified_by = Column(String(255), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)

    ingredient = relationship("Ingredient", back_populates="nutrients")

