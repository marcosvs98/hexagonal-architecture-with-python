from enum import Enum
from typing import TYPE_CHECKING, List
from pydantic import Field
from domain.base.event import DomainEvent
from domain.maps.value_objects import Address

from domain.payment.value_objects import PaymentId
from domain.order.value_objects import OrderId
from domain.order.value_objects import BuyerId
from domain.order.value_objects import OrderLine


class OrderCreated(DomainEvent):
    event_name: str = Field('payment_order_created')
    order_id: OrderId
    buyer_id: BuyerId
    lines: List[OrderLine]
    product_cost: float
    delivery_cost: float
    payment_id: PaymentId
    destination: Address
    version: int = 0


class OrderPaid(DomainEvent):
    event_name: str = Field('payment_order_paid')
    order_id: OrderId
    buyer_id: BuyerId
    lines: List[OrderLine]
    product_cost: float
    delivery_cost: float
    payment_id: PaymentId
    version: int = 0


class OrderCancelled(DomainEvent):
    event_name: str = Field('payment_order_cancelled')
    order_id: OrderId
    buyer_id: BuyerId
    lines: List[OrderLine]
    product_cost: float
    delivery_cost: float
    payment_id: PaymentId
    version: int = 0


class OrderEvent(Enum):
    """Domain Event raised for special order use cases"""
    CREATED = 'CREATED'
    CANCELLED = 'CANCELLED'
    PAID = 'PAID'