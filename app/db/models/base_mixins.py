import uuid
import copy
from typing import Dict, List, Tuple
from datetime import datetime

from sqlalchemy import func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from app.core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.metadata_naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    def serialize(
        self, 
        schema_class,
        model_dump: bool = False,
        exclude_fields: List[str | None] | Tuple[str | None] = [],
    ) -> Dict:
        serialized_data = {}
        schema_fields = schema_class.model_fields.keys()
        data = copy.deepcopy(self.__dict__)
        
        for field in schema_fields:
            serialized_data[field] = data.get(field) # Добавляем не указаным полям значение None
        
        if not exclude_fields:
            return serialized_data
       
        for field in exclude_fields: 
            serialized_data.pop(field)

        if model_dump:
            return serialized_data
  
        return schema_class(**serialized_data)


class TimestampedMixin:
    """Миксин для даты создания и даты обновления"""

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
