from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.db.models import Order, OrderItem
from app.schemas.order import OrderSchema
from app.schemas.order_item import OrderItemSchema
from app.core.config import settings
from .http import get_response_data_or_raise_http_exception
from app.services import ProductHttpService
from app.core.container import Container


@inject
async def serialize_order(
    order: Order,
    model_dump: bool = False,
    items: list['OrderItem'] | None = None,
    product_http_service: ProductHttpService = Depends(
        Provide[Container.product_http_service]
    )
) -> dict | OrderSchema:
    """_summary_

    Args:
        model_dump (bool, optional): _description_. Defaults to False.
        items (list[OrderItem] | None, optional): 
            Передается если в запросе не был выполнен join 
            на Order.items.
            ОБЯЗАТЕЛЬНО доставать Order.items вместе с OrderItem.product
                
            Пример запроса в app.repositories.order.py,
            класс RepositoryOrder, метод get: load_items_with_products=True
                 
        Defaults to None.

    Returns:
        dict | OrderSchema
    """
    if not items:
        items = order.items
            
    products_ids = [item.product_id for item in items]
    products_data = await product_http_service.get_products_by_ids(products_ids)
            
    items_schemas = [
        OrderItemSchema(
            id=item.id,
            product=products_data[index],
            product_quantity=item.product_quantity
        ) for index, item in enumerate(items)
    ]
        
    order_schema = OrderSchema(
        id=order.id,
        status=order.status,
        user_id=order.user_id,
        items=items_schemas
    )
        
    if model_dump:
        return order_schema.model_dump()
        
    return order_schema