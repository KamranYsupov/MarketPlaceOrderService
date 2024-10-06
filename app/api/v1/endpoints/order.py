from uuid import UUID
from typing import List, Dict, Any

from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

from app.core.container import Container
from app.schemas.order import (
    OrderSchema,
    CreateOrderSchema,
    OrderStatusSchema,
)
from app.schemas.order_item import (
    OrderItemSchema,
    CreateOrderItemSchema
)
from app.utils.enums import OrderStatus
from app.utils.serializers import serialize_order
from app.services import OrderService
from app.db.models import Order
from ..deps import get_current_user


router = APIRouter(tags=['Order'], prefix='/orders')


@router.get(
    '/{order_id}',
    status_code=status.HTTP_200_OK,
    response_model=OrderSchema,
    response_model_exclude_none=True,
)
@inject
async def get_order(
    order_id: UUID,
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(
        Provide[Container.order_service]
    ),
) -> OrderSchema:
    order = await order_service.get(
        id=order_id,
        load_items=True
    )    
    order_schema = await serialize_order(order)
    
    return order_schema


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[OrderSchema],
    response_model_exclude_none=True,
)
@inject
async def get_orders(
    limit: int = 10,
    skip: int = 0, 
    order_service: OrderService = Depends(
        Provide[Container.order_service]
    ),
) -> List[OrderSchema]:
    orders = await order_service.orders_list(
        limit=limit,
        skip=skip,
        load_items=True
    )    
    order_schemas = [await serialize_order(order) for order in orders]
    
    return order_schemas


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=OrderSchema,
    response_model_exclude_none=True,
)
@inject
async def create_order(
    create_order_schema: CreateOrderSchema,
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(
        Provide[Container.order_service]
    ),
) -> OrderSchema:
    create_order_schema.user_id = UUID(user['id'])
    order = await order_service.create_order(
        obj_in=create_order_schema,
        access_token=user['access_token']
    )
    
    items = await order_service.items_list(
        order_id=order.id,
        load_orders=False,
    )
    order_schema = await serialize_order(order=order, items=items)

    return order_schema


@router.put(
    '/{order_id}/status',
    status_code=status.HTTP_200_OK,
)
@inject
async def update_order_status(
    order_id: UUID,
    status: OrderStatusSchema, 
    order_service: OrderService = Depends(
        Provide[Container.order_service]
    ),
) -> dict[str, str]:
    order = await order_service.update(
        obj_id=order_id,
        obj_in=status.model_dump(),
    )    
    
    return {'message': 'Статус успешно обновлен'}