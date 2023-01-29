from enum import Enum
from typing import TYPE_CHECKING

from domain.base.event import DomainEvent
from domain.base.model import Attribute
from domain.maps.value_objects import Address
from domain.product.value_objects import PriceThb
from domain.payment.value_objects import PaymentId

from domain.order.value_objects import OrderId
from domain.order.value_objects import BuyerId
from domain.order.value_objects import OrderLineList



class OrderCreated(DomainEvent):
    event_name: str = Attribute(default='payment_order_created')
    order_id: OrderId = Attribute()
    buyer_id: BuyerId = Attribute()
    lines: OrderLineList = Attribute()
    product_cost: PriceThb = Attribute()
    delivery_cost: PriceThb = Attribute()
    payment_id: PaymentId = Attribute()
    destination: Address = Attribute()
    version: int = Attribute(default=0)

    if TYPE_CHECKING:
        def __init__(self, order_id: OrderId, buyer_id: BuyerId, lines: OrderLineList,
                     product_cost: PriceThb, delivery_cost: PriceThb, payment_id: PaymentId, destination: Address):
            super().__init__()


class OrderPaid(DomainEvent):
    event_name: str = Attribute(default='payment_order_paid')
    order_id: OrderId = Attribute()
    buyer_id: BuyerId = Attribute()
    lines: OrderLineList = Attribute()
    product_cost: PriceThb = Attribute()
    delivery_cost: PriceThb = Attribute()
    payment_id: PaymentId = Attribute()
    version: int = Attribute(default=0)

    if TYPE_CHECKING:
        def __init__(self, *, order_id: OrderId, buyer_id: BuyerId, lines: OrderLineList,
                     product_cost: PriceThb, delivery_cost: PriceThb, payment_id: PaymentId):
            super().__init__()


class OrderCancelled(DomainEvent):
    event_name: str = Attribute(default='payment_order_cancelled')
    order_id: OrderId = Attribute()
    buyer_id: BuyerId = Attribute()
    lines: OrderLineList = Attribute()
    product_cost: PriceThb = Attribute()
    delivery_cost: PriceThb = Attribute()
    payment_id: PaymentId = Attribute()
    version: int = Attribute(default=0)

    if TYPE_CHECKING:
        def __init__(self, *, order_id: OrderId, buyer_id: BuyerId, lines: OrderLineList,
                     product_cost: PriceThb, delivery_cost: PriceThb, payment_id: PaymentId):
            super().__init__()



class OrderEvent(Enum):
    """Domain Event raised for special order use cases"""
    CREATED = 'CREATED'
    CANCELLED = 'CANCELLED'
    PAID = 'PAID'