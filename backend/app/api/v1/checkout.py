import random
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, log_audit_event
from app.core.errors import BadRequestException
from app.db.session import get_db
import app.db.models as models
from app.schemas.commerce import CheckoutRequest, OrderResponse

router = APIRouter(prefix="/checkout", tags=["checkout"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def checkout_cart(
    payload: CheckoutRequest,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Executes demo sandbox checkout in a database transaction, creating an immutable prototype order."""
    # 1. Fetch User Cart
    cart_stmt = select(models.Cart).where(models.Cart.user_id == current_user.id)
    cart = (await db.execute(cart_stmt)).scalar_one_or_none()
    if not cart:
        raise BadRequestException("EMPTY_CART", "Your cart is empty.")

    # 2. Fetch Cart Items with Formulations
    items_stmt = (
        select(models.CartItem, models.ProductFormulation, models.ProductCategory)
        .join(models.ProductFormulation, models.CartItem.formulation_id == models.ProductFormulation.id)
        .join(models.ProductCategory, models.ProductFormulation.category_id == models.ProductCategory.id)
        .where(models.CartItem.cart_id == cart.id)
    )
    cart_rows = (await db.execute(items_stmt)).all()
    if not cart_rows:
        raise BadRequestException("EMPTY_CART", "No items found in your cart.")

    # 3. Compute Totals Deterministically
    subtotal = 0.0
    for ci, form, _ in cart_rows:
        subtotal += float(form.cost_per_pack_inr) * ci.quantity

    subtotal = round(subtotal, 2)
    delivery_fee = 0.0 if subtotal > 300.0 else 40.0
    total = round(subtotal + delivery_fee, 2)

    # 4. Generate Order Number: NAI-2026-XXXXXX
    rand_suffix = f"{random.randint(100000, 999999)}"
    order_number = f"NAI-2026-{rand_suffix}"

    # 5. Create Order Record
    order = models.Order(
        order_number=order_number,
        user_id=current_user.id,
        status="confirmed",
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        total=total,
        shipping_address=payload.shipping_address.model_dump(),
        payment_mode="demo_sandbox",
        is_prototype=True,
    )
    db.add(order)
    await db.flush()

    # 6. Create Order Items (Snapshots)
    order_item_responses = []
    for ci, form, cat in cart_rows:
        unit_p = float(form.cost_per_pack_inr)
        item_tot = round(unit_p * ci.quantity, 2)
        prod_name = cat.name.get("en", "Prototype Product")

        oi = models.OrderItem(
            order_id=order.id,
            formulation_id=form.id,
            product_name=prod_name,
            unit_price=unit_p,
            quantity=ci.quantity,
            total_price=item_tot,
        )
        db.add(oi)
        await db.flush()

        order_item_responses.append({
            "id": oi.id,
            "formulation_id": form.id,
            "product_name": prod_name,
            "unit_price": unit_p,
            "quantity": ci.quantity,
            "total_price": item_tot,
        })

        # Also auto-create a Consumption Plan for the user so they can start tracking immediately!
        plan = models.ConsumptionPlan(
            user_id=current_user.id,
            formulation_id=form.id,
            order_item_id=oi.id,
            total_servings=form.pack_size_servings * ci.quantity,
            daily_target_servings=1,
            status="active",
        )
        db.add(plan)

    # 7. Initial Lifecycle Status Event
    status_event = models.OrderStatusEvent(
        order_id=order.id,
        status="confirmed",
        note="Demo sandbox payment authorized. Prototype batch queued.",
    )
    db.add(status_event)

    # 8. Empty the Cart
    for ci, _, _ in cart_rows:
        await db.delete(ci)

    await db.commit()
    await db.refresh(order)

    await log_audit_event(
        db,
        current_user.id,
        action="order_placed_sandbox",
        resource_type="orders",
        resource_id=str(order.id),
        details={"order_number": order_number, "total": total},
    )

    return OrderResponse(
        id=order.id,
        order_number=order.order_number,
        status=order.status,
        subtotal=float(order.subtotal),
        delivery_fee=float(order.delivery_fee),
        total=float(order.total),
        shipping_address=order.shipping_address,
        payment_mode=order.payment_mode,
        is_prototype=order.is_prototype,
        items=order_item_responses,
        status_events=[
            {
                "status": status_event.status,
                "note": status_event.note,
                "created_at": status_event.created_at,
            }
        ],
        created_at=order.created_at,
    )

