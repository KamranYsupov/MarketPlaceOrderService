from uuid import UUID
from typing import List, Optional, TYPE_CHECKING

from pydantic import BaseModel
      
from app.utils.enums import OrderStatus
from .order_item import OrderItemSchema, CreateOrderItemSchema
    
    
class OrderStatusSchema(BaseModel):
    status: OrderStatus = OrderStatus.IN_PROGRESS
    
    
class OrderUserIdSchema(BaseModel):
    user_id: UUID
    

class OrderBaseSchema(OrderStatusSchema, OrderUserIdSchema):
    pass

 
class OrderSchema(OrderBaseSchema):
    id: UUID
    items: Optional[List[OrderItemSchema]] = None
    
    
class CreateOrderSchema(OrderBaseSchema):
    items: List[CreateOrderItemSchema] 
    
    

     

    

    
