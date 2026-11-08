import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.core.errors import NotFoundException
from app.db.session import get_db
import app.db.models as models
from app.schemas.commerce import (
    AddToCartRequest,
    CartItemResponse,
    CartResponse,
    UpdateCartItemRequest,
)

router = APIRouter(prefix="/cart", tags=["cart"])


async def get_or_create_user_cart(user_id: uuid.UUID, db: AsyncSession) -> models.Cart:
    stmt = select(models.Cart).where(models.Cart.user_id == user_id)
    cart = (await db.execute(stmt)).scalar_one_or_none()
    if not cart:
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        await db.commit()
        await db.refresh(cart)
    return cart


@router.get("/items", response_model=CartResponse)
async def get_cart(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cart = await get_or_create_user_cart(current_user.id, db)

    # Fetch cart items with product formulations
    stmt = (
        select(models.CartItem, models.ProductFormulation, models.ProductCategory)
        .join(models.ProductFormulation, models.CartItem.formulation_id == models.ProductFormulation.id)
        .join(models.ProductCategory, models.ProductFormulation.category_id == models.ProductCategory.id)
        .where(models.CartItem.cart_id == cart.id)
    )
    res = await db.execute(stmt)
    rows = res.all()

    items = []
    subtotal = 0.0

    for ci, form, cat in rows:
        unit_price = float(form.cost_per_pack_inr)
        item_total = round(unit_price * ci.quantity, 2)
        subtotal += item_total

        items.append(
            CartItemResponse(
                id=ci.id,
                formulation_id=form.id,
                product_name=cat.name.get("en", "Prototype Formulation"),
                category_slug=cat.slug,
                unit_price=unit_price,
                quantity=ci.quantity,
                subtotal=item_total,
                pack_size_servings=form.pack_size_servings,
            )
        )

    subtotal = round(subtotal, 2)
    delivery_fee = 0.0 if subtotal > 300.0 or subtotal == 0.0 else 40.0
    total = round(subtotal + delivery_fee, 2)

    return CartResponse(
        id=cart.id,
        items=items,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        total=total,
        is_prototype=True,
        prototype_badge="Prototype product – demo checkout",
    )


@router.post("/items", status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    payload: AddToCartRequest,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cart = await get_or_create_user_cart(current_user.id, db)

    # Verify formulation exists
    form_stmt = select(models.ProductFormulation).where(models.ProductFormulation.id == payload.formulation_id)
    form = (await db.execute(form_stmt)).scalar_one_or_none()
    if not form:
        raise NotFoundException("Product Formulation", payload.formulation_id)

    # Check if item already exists in cart
    ci_stmt = select(models.CartItem).where(models.CartItem.cart_id == cart.id, models.CartItem.formulation_id == payload.formulation_id)
    existing_ci = (await db.execute(ci_stmt)).scalar_one_or_none()

    if existing_ci:
        existing_ci.quantity += payload.quantity
    else:
        new_ci = models.CartItem(
            cart_id=cart.id,
            formulation_id=payload.formulation_id,
            quantity=payload.quantity,
        )
        db.add(new_ci)

    await db.commit()
    return {"success": True, "message": "Product added to cart."}


@router.patch("/items/{id}")
async def update_cart_item(
    id: uuid.UUID,
    payload: UpdateCartItemRequest,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cart = await get_or_create_user_cart(current_user.id, db)

    ci_stmt = select(models.CartItem).where(models.CartItem.id == id, models.CartItem.cart_id == cart.id)
    ci = (await db.execute(ci_stmt)).scalar_one_or_none()
    if not ci:
        raise NotFoundException("Cart Item", id)

    ci.quantity = payload.quantity
    await db.commit()
    return {"success": True, "message": "Cart quantity updated."}


@router.delete("/items/{id}")
async def remove_cart_item(
    id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cart = await get_or_create_user_cart(current_user.id, db)

    ci_stmt = select(models.CartItem).where(models.CartItem.id == id, models.CartItem.cart_id == cart.id)
    ci = (await db.execute(ci_stmt)).scalar_one_or_none()
    if not ci:
        raise NotFoundException("Cart Item", id)

    await db.delete(ci)
    await db.commit()
    return {"success": True, "message": "Item removed from cart."}

