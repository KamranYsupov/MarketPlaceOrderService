from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import Base, TimestampedMixin
from app.schemas.order import OrderSchema
from app.schemas.order_item import OrderItemSchema
from app.utils.enums import OrderStatus
from app.core.config import settings


class Order(Base, TimestampedMixin):
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        nullable=False
    ) 
    user_id: Mapped[UUID] 
    
    items: Mapped[list['OrderItem']] = relationship(
        back_populates='order',
        lazy='selectin',
    )
    

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    order_id: Mapped[UUID] = mapped_column(
        ForeignKey('orders.id', ondelete='CASCADE'), index=True,
    )
    product_id: Mapped[UUID]
    product_quantity: Mapped[int]
    
    order: Mapped[Order] = relationship(
        back_populates='items',
        lazy='joined',
    )