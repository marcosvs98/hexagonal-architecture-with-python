import abc
from sqlalchemy.orm import Session

from domain.order.value_objects import OrderId
from domain.order.entities import Order


class OrderDatabaseInterface(abc.ABC):
    db_session: Session

    @abc.abstractmethod
    async def next_identity(self) -> OrderId:
        raise NotImplementedError

    @abc.abstractmethod
    async def from_id(self, id_: OrderId) -> Order:
        raise NotImplementedError

    @abc.abstractmethod
    async def save(self, entity: Order):
        raise NotImplementedError
