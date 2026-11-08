from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class Cart(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "carts"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "cart_items"

    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id", ondelete="CASCADE"), nullable=False, index=True)
    formulation_id = Column(UUID(as_uuid=True), ForeignKey("product_formulations.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    cart = relationship("Cart", back_populates="items")
    formulation = relationship("ProductFormulation")


class Order(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orders"

    order_number = Column(String(32), unique=True, nullable=False, index=True)  # NAI-2026-000123
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(
        Enum("pending", "confirmed", "processing", "shipped", "delivered", "cancelled", name="order_status_enum"),
        default="pending",
        nullable=False,
        index=True,
    )
    subtotal = Column(Numeric(10, 2), nullable=False)
    delivery_fee = Column(Numeric(10, 2), default=0.0, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    shipping_address = Column(JSONB, nullable=False)  # Snapshot
    payment_mode = Column(String(32), default="demo_sandbox", nullable=False)
    is_prototype = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    status_events = relationship("OrderStatusEvent", back_populates="order", cascade="all, delete-orphan", order_by="OrderStatusEvent.created_at")


class OrderItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "order_items"

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    formulation_id = Column(UUID(as_uuid=True), ForeignKey("product_formulations.id", ondelete="RESTRICT"), nullable=False)
    product_name = Column(String(255), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    formulation = relationship("ProductFormulation")


class OrderStatusEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "order_status_events"

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(32), nullable=False)
    note = Column(Text, nullable=True)

    order = relationship("Order", back_populates="status_events")

