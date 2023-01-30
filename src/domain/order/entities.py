from pydantic.fields import Field
from pydantic import validator
from typing import TYPE_CHECKING, List

from domain.base.entity import Entity
from domain.payment.value_objects import PaymentId
from domain.order.value_objects import OrderId
from domain.order.value_objects import BuyerId
from domain.order.value_objects import OrderLine
from domain.order.value_objects import OrderStatus, OrderStatusEnum
from domain.order.events import OrderPaid, OrderCancelled
from exceptions import CommonException

class OrderAlreadyCancelledException(CommonException):
    pass


class OrderAlreadyPaidException(CommonException):
    pass


class PaymentNotVerifiedException(CommonException):
    pass


class Order(Entity):
    order_id: OrderId# = Attribute()
    buyer_id: BuyerId# = Attribute()
    lines: List[OrderLine]#OrderLineList# = Attribute()
    product_cost: float #PriceThb# = Attribute()
    delivery_cost: float #PriceThb# = Attribute()
    payment_id: PaymentId# = Attribute()
    status: OrderStatus = OrderStatus.Enum.WAITING
    version: int = 0

    def pay(self, is_payment_verified: bool):
        if self.is_cancelled():
            raise OrderAlreadyCancelledException(detail='Order\'s already cancelled')
        if self.is_paid():
            raise OrderAlreadyPaidException(detail='Order\'s already paid')
        if not is_payment_verified:
            raise PaymentNotVerifiedException(detail=f'Payment {self.payment_id} must be verified')

        self.status = OrderStatus.Enum.PAID

    def cancel(self):
        if self.is_cancelled():
            raise OrderAlreadyCancelledException(detail='Order\'s already cancelled')
        if self.is_paid():
            raise OrderAlreadyPaidException(detail='Order\'s already paid')

        self.status = OrderStatus.Enum.CANCELLED

    def is_waiting(self) -> bool:
        return self._get_order_status(self.status).is_waiting()

    def is_paid(self) -> bool:
        return self._get_order_status(self.status).is_paid()

    def is_cancelled(self) -> bool:
        return self._get_order_status(self.status).is_cancelled()

    def _get_order_status(self, value):
        return OrderStatus(value)

    @property
    def total_cost(self) -> float:
        return self.product_cost + self.delivery_cost

    def increase_version(self):
        self.version += 1

    class Config:
        arbitrary_types_allowed = True