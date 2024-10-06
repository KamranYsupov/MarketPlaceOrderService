import uuid
from typing import List, Optional, Union, Sequence

from fastapi import HTTPException
from starlette import status

from .mixins import CRUDServiceMixin
from app.repositories.order import (
    RepositoryOrder,
    RepositoryOrderItem
)
from .product import ProductHttpService
from app.db.models import Order, OrderItem
from app.schemas.order import OrderSchema, CreateOrderSchema
from app.schemas.order_item import OrderItemSchema


class OrderService(CRUDServiceMixin):
    def __init__(
        self, 
        repository_order: RepositoryOrder,
        repository_order_item: RepositoryOrder,
        product_http_service: ProductHttpService,
        unique_fields: Union[Sequence[str], None] = None,
    ):
        self._repository_order = repository_order
        self._repository_order_item = repository_order_item
        self._product_http_service = product_http_service

        super().__init__(
            repository=repository_order,
            unique_fields=unique_fields,
        )
        
    async def orders_list( 
        self,
        *args,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        load_items: bool = False,
        **kwargs
    ):
        return await self._repository_order.list(
            *args, 
            limit=limit, 
            skip=skip,
            load_items=load_items,
            **kwargs,
        )
        
    async def get_order(
        self,
        load_items: bool = False,
        **kwargs
    ):
        return await self._repository_order.get(
            load_items=load_items,
            **kwargs
        )
        
    async def create_order(self, obj_in: CreateOrderSchema, access_token: str) -> Order:
        order_data = dict(obj_in)
        order_data['id'] = uuid.uuid4()
        items_schemas = order_data.pop('items')
        
        products_ids = [item.product_id for item in items_schemas]
        products_data = await self._product_http_service.get_products_by_ids(
            ids=products_ids
        )
        product_dict = {product['id']: product for product in products_data}
        
        for item in items_schemas:
            product = product_dict.get(str(item.product_id))
            updated_quantity = product['quantity'] - item.product_quantity
            
            if updated_quantity < 0:
                raise HTTPException(
                    detail='Недостаточно товара на складе',
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
                
            product['quantity'] = updated_quantity
            item.order_id = order_data['id']
            
            if isinstance(item.product_id, str):
                item.product_id = uuid.UUID(item.product_id)
        
        order = await self._repository_order.create(order_data)
        await self._repository_order_item.bulk_create(items_schemas)
        await self._product_http_service.bulk_update(products_data, access_token)
        
        return order
    
    async def items_list(
        self,
        *args,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        load_orders: bool = False,
        load_products: bool = False,
        **kwargs
    ) -> List[OrderItem]:
        return await self._repository_order_item.list(
            *args,
            limit=limit,
            skip=skip,
            load_orders=load_orders,
            **kwargs
        )
                
        
        
        
        
        
                
