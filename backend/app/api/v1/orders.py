import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import check_resource_ownership, get_current_user, log_audit_event
from app.core.errors import BadRequestException, NotFoundException
from app.db.session import get_db
import app.db.models as models
from app.schemas.commerce import OrderItemResponse, OrderResponse, OrderStatusEventResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=List[OrderResponse])
async def list_orders(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(models.Order)
        .where(models.Order.user_id == current_user.id)
        .order_by(desc(models.Order.created_at))
    )
    res = await db.execute(stmt)
    orders = res.scalars().all()

    response_list = []
    for o in orders:
        # Items
        items_stmt = select(models.OrderItem).where(models.OrderItem.order_id == o.id)
        items = (await db.execute(items_stmt)).scalars().all()

        # Events
        events_stmt = select(models.OrderStatusEvent).where(models.OrderStatusEvent.order_id == o.id).order_by(models.OrderStatusEvent.created_at)
        events = (await db.execute(events_stmt)).scalars().all()

        response_list.append(
            OrderResponse(
                id=o.id,
                order_number=o.order_number,
                status=o.status,
                subtotal=float(o.subtotal),
                delivery_fee=float(o.delivery_fee),
                total=float(o.total),
                shipping_address=o.shipping_address,
                payment_mode=o.payment_mode,
                is_prototype=o.is_prototype,
                items=[
                    OrderItemResponse(
                        id=it.id,
                        formulation_id=it.formulation_id,
                        product_name=it.product_name,
                        unit_price=float(it.unit_price),
                        quantity=it.quantity,
                        total_price=float(it.total_price),
                    )
                    for it in items
                ],
                status_events=[
                    OrderStatusEventResponse(
                        status=ev.status,
                        note=ev.note,
                        created_at=ev.created_at,
                    )
                    for ev in events
                ],
                created_at=o.created_at,
            )
        )

    return response_list


@router.get("/{id}", response_model=OrderResponse)
async def get_order_detail(
    id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.Order).where(models.Order.id == id)
    res = await db.execute(stmt)
    order = res.scalar_one_or_none()
    if not order:
        raise NotFoundException("Order", id)

    check_resource_ownership(order.user_id, current_user)

    items_stmt = select(models.OrderItem).where(models.OrderItem.order_id == order.id)
    items = (await db.execute(items_stmt)).scalars().all()

    events_stmt = select(models.OrderStatusEvent).where(models.OrderStatusEvent.order_id == order.id).order_by(models.OrderStatusEvent.created_at)
    events = (await db.execute(events_stmt)).scalars().all()

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
        items=[
            OrderItemResponse(
                id=it.id,
                formulation_id=it.formulation_id,
                product_name=it.product_name,
                unit_price=float(it.unit_price),
                quantity=it.quantity,
                total_price=float(it.total_price),
            )
            for it in items
        ],
        status_events=[
            OrderStatusEventResponse(
                status=ev.status,
                note=ev.note,
                created_at=ev.created_at,
            )
            for ev in events
        ],
        created_at=order.created_at,
    )


@router.post("/{id}/cancel")
async def cancel_order(
    id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.Order).where(models.Order.id == id)
    res = await db.execute(stmt)
    order = res.scalar_one_or_none()
    if not order:
        raise NotFoundException("Order", id)

    check_resource_ownership(order.user_id, current_user)

    if order.status in ("shipped", "delivered", "cancelled"):
        raise BadRequestException("CANNOT_CANCEL", f"Order cannot be cancelled in state '{order.status}'.")

    order.status = "cancelled"
    event = models.OrderStatusEvent(
        order_id=order.id,
        status="cancelled",
        note="Order cancelled by user.",
    )
    db.add(event)
    await db.commit()

    await log_audit_event(
        db,
        current_user.id,
        action="order_cancelled",
        resource_type="orders",
        resource_id=str(order.id),
    )

    return {"success": True, "message": "Order has been cancelled."}

