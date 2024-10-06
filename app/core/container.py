from dependency_injector import containers, providers

from app.repositories import (
    RepositoryOrder,
    RepositoryOrderItem,
)
from app.services import (
    OrderService,
    ProductHttpService
)
from app.db import DataBaseManager
from app.db.models import (
    Order,
    OrderItem,
)
from app.core.config import settings


class Container(containers.DeclarativeContainer):
    db_manager = providers.Singleton(DataBaseManager, db_url=settings.db_url)
    session = providers.Resource(db_manager().get_async_session)

    # region repository
    repository_order = providers.Singleton(
        RepositoryOrder, model=Order, session=session
    )
    repository_order_item = providers.Singleton(
        RepositoryOrderItem, model=OrderItem, session=session
    )
    # endregion

    # region services
    product_http_service = providers.Singleton(
        ProductHttpService
    )
    order_service = providers.Singleton(
        OrderService,
        product_http_service=product_http_service,
        repository_order=repository_order,
        repository_order_item=repository_order_item,
    )
    
    # endregion


container = Container()
container.init_resources()
container.wire(modules=settings.container_wiring_modules)
