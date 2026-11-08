from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class ProductCategory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_categories"

    slug = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(JSONB, nullable=False)  # {"en": "Roasted Millet Energy Bar", "ta": "...", ...}
    format_template = Column(JSONB, nullable=False)  # {"serving_size_g": 35.0, "binder_min_pct": 15.0, ...}
    description = Column(JSONB, nullable=False)

    formulations = relationship("ProductFormulation", back_populates="category")


class ProductFormulation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_formulations"
    __table_args__ = (
        UniqueConstraint("formulation_code", "version", name="uq_formulation_code_version"),
    )

    formulation_code = Column(String(64), nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("product_categories.id", ondelete="RESTRICT"), nullable=False)
    serving_size_g = Column(Numeric(6, 2), nullable=False)
    nutrient_results_per_serving = Column(JSONB, nullable=False)
    cost_per_serving_inr = Column(Numeric(6, 2), nullable=False)
    cost_per_pack_inr = Column(Numeric(6, 2), nullable=False)
    pack_size_servings = Column(Integer, default=14, nullable=False)
    solver_status = Column(String(32), default="optimal", nullable=False)
    constraints_snapshot = Column(JSONB, default=dict, nullable=False)
    validation_status = Column(
        Enum("computed_only", "expert_reviewed", "lab_validated", name="formulation_validation_status_enum"),
        default="computed_only",
        nullable=False,
    )
    preparation_instructions = Column(JSONB, default=dict, nullable=False)
    storage_instructions = Column(JSONB, default=dict, nullable=False)

    category = relationship("ProductCategory", back_populates="formulations")
    ingredients = relationship("FormulationIngredient", back_populates="formulation", cascade="all, delete-orphan")
    recommendations = relationship("GeneratedRecommendation", back_populates="formulation")


class FormulationIngredient(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "formulation_ingredients"

    formulation_id = Column(UUID(as_uuid=True), ForeignKey("product_formulations.id", ondelete="CASCADE"), nullable=False, index=True)
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id", ondelete="RESTRICT"), nullable=False, index=True)
    ingredient_version = Column(Integer, default=1, nullable=False)
    grams_per_serving = Column(Numeric(6, 2), nullable=False)
    pct_of_mix = Column(Numeric(5, 2), nullable=False)
    purpose = Column(
        Enum("iron_source", "absorption_enhancer", "folate_source", "b12_source", "protein", "binder", "flavour", "bulk", name="ingredient_purpose_enum"),
        default="iron_source",
        nullable=False,
    )
    rationale_code = Column(String(64), nullable=False)

    formulation = relationship("ProductFormulation", back_populates="ingredients")
    ingredient = relationship("Ingredient")


class ProductImage(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_images"

    formulation_id = Column(UUID(as_uuid=True), ForeignKey("product_formulations.id", ondelete="SET NULL"), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("product_categories.id", ondelete="SET NULL"), nullable=True)
    storage_key = Column(String(512), nullable=False)
    alt_text = Column(JSONB, default=dict, nullable=False)
    is_illustrative = Column(Boolean, default=True, nullable=False)

