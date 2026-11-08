import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AddToCartRequest(BaseModel):
    formulation_id: uuid.UUID
    quantity: int = Field(default=1, ge=1, le=50)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(ge=1, le=50)


class CartItemResponse(BaseModel):
    id: uuid.UUID
    formulation_id: uuid.UUID
    product_name: str
    category_slug: str
    unit_price: float
    quantity: int
    subtotal: float
    pack_size_servings: int


class CartResponse(BaseModel):
    id: uuid.UUID
    items: List[CartItemResponse] = Field(default_factory=list)
    subtotal: float
    delivery_fee: float
    total: float
    is_prototype: bool = True
    prototype_badge: str = "Prototype product – demo checkout"


class ShippingAddress(BaseModel):
    full_name: str
    phone: str
    address_line: str
    city: str
    state: str
    pin_code: str = Field(pattern=r"^[1-9][0-9]{5}$")


class CheckoutRequest(BaseModel):
    shipping_address: ShippingAddress
    payment_mode: str = Field(default="demo_sandbox")


class OrderStatusEventResponse(BaseModel):
    status: str
    note: Optional[str] = None
    created_at: datetime


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    formulation_id: uuid.UUID
    product_name: str
    unit_price: float
    quantity: int
    total_price: float


class OrderResponse(BaseModel):
    id: uuid.UUID
    order_number: str
    status: str
    subtotal: float
    delivery_fee: float
    total: float
    shipping_address: Dict[str, Any]
    payment_mode: str
    is_prototype: bool = True
    items: List[OrderItemResponse] = Field(default_factory=list)
    status_events: List[OrderStatusEventResponse] = Field(default_factory=list)
    created_at: datetime

