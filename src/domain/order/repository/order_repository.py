from uuid import uuid4


from typing import Dict

from sqlalchemy.orm import Session
#from database.models import Order as OrderORM
from domain.order.ports.order_database_interface import OrderDatabaseInterface  # noqa: E501
from domain.order.value_objects import OrderId
from domain.order.entities import Order
from exceptions import CommonException

class EntityNotFound(CommonException):
    pass


class EntityOutdated(CommonException):
    pass


class OrderRepository(OrderDatabaseInterface):
    db_session: Session
    #order_model = OrderORM

    def __init__(self):
        self._storage: Dict[OrderId, Order] = {}

    async def next_identity(self) -> OrderId:
        return OrderId(str(uuid4()))

    async def from_id(self, order_id: OrderId) -> Order:
        try:
            return self._storage[order_id]
        except KeyError:
            raise EntityNotFound(detail=f'Order with OrderId {str(order_id)} not found')

    async def save(self, entity: Order):
        order_id = entity.order_id
        try:
            old = self._storage[order_id]
        except KeyError:
            self._storage[order_id] = entity
            return

        entity.increase_version()
        if old.version > entity.version:
            raise EntityOutdated(detail=f'Order with OrderId {str(order_id)} is not dated')

        self._storage[order_id] = entity
