from typing import TYPE_CHECKING

#from domain.model.registry import DomainRegistry
from domain.base.entity import Entity
from domain.base.model import Attribute, AttributeSetter

from domain.product.value_objects import PriceThb
from domain.payment.value_objects import PaymentId

from domain.order.value_objects import OrderId
from domain.order.value_objects import BuyerId
from domain.order.value_objects import OrderLineList
from domain.order.value_objects import OrderStatus
from domain.order.events import OrderPaid, OrderCancelled
from exceptions import CommonException

class OrderAlreadyCancelledException(CommonException):
    pass


class OrderAlreadyPaidException(CommonException):
    pass


class PaymentNotVerifiedException(CommonException):
    pass


class Order(Entity):
    order_id: OrderId = Attribute()
    buyer_id: BuyerId = Attribute()
    lines: OrderLineList = Attribute()
    product_cost: PriceThb = Attribute()
    delivery_cost: PriceThb = Attribute()
    payment_id: PaymentId = Attribute()
    status: OrderStatus = Attribute(default=OrderStatus.Enum.WAITING)
    version: int = Attribute(default=0)

    def pay(self, is_payment_verified: bool):
        if self.is_cancelled():
            raise OrderAlreadyCancelledException(detail='Order\'s already cancelled')
        if self.is_paid():
            raise OrderAlreadyPaidException(detail='Order\'s already paid')
        if not is_payment_verified:
            raise PaymentNotVerifiedException(detail=f'Payment {self.payment_id} must be verified')

        self._status = OrderStatus(OrderStatus.Enum.PAID)

    def cancel(self):
        if self.is_cancelled():
            raise OrderAlreadyCancelledException(detail='Order\'s already cancelled')
        if self.is_paid():
            raise OrderAlreadyPaidException(detail='Order\'s already paid')

        self._status = OrderStatus(OrderStatus.Enum.CANCELLED)

    def is_waiting(self) -> bool:
        return self._status.is_waiting()

    def is_paid(self) -> bool:
        return self._status.is_paid()

    def is_cancelled(self) -> bool:
        return self._status.is_cancelled()

    @property
    def total_cost(self) -> PriceThb:
        return PriceThb(self._product_cost + self._delivery_cost)

    def increase_version(self):
        self._version += 1

    if TYPE_CHECKING:
        def __init__(self, *, order_id: OrderId, buyer_id: BuyerId, lines: OrderLineList,
                     product_cost: PriceThb, delivery_cost: PriceThb, payment_id: PaymentId,
                     status: OrderStatus = OrderStatus.Enum.WAITING, version: int = 0):
            super().__init__()

    _order_id: OrderId = AttributeSetter()
    _buyer_id: BuyerId = AttributeSetter()
    _lines: OrderLineList = AttributeSetter()
    _product_cost: PriceThb = AttributeSetter()
    _delivery_cost: PriceThb = AttributeSetter()
    _payment_id: PaymentId = AttributeSetter()
    _status: OrderStatus = AttributeSetter()
    _version: int = AttributeSetter()