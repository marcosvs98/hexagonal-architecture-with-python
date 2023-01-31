import uuid
from typing import List
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel

from domain.order.entities import Order as DomainOrder
from domain.order.value_objects import OrderId


class Address(BaseModel):
    house_number: str
    road: str
    sub_district: str
    district: str
    province: str
    postcode: str
    country: str

    class Config:
        schema_extra = {
            'example': {
                'house_number': '123',
                'road': 'ROAD',
                'sub_district': 'SUB_DISTRICT',
                'district': 'DISTRICT',
                'province': 'bangkok',
                'postcode': '10123',
                'country': 'THAILAND',
            }
        }


class OrderLine(BaseModel):
    product_id: str
    amount: int

    class Config:
        schema_extra = {
            'example': {
                'product_id': str(ObjectId()),
                'amount': 20,
            }
        }


class OrderCreateRequest(BaseModel):
    buyer_id: str
    lines: List[OrderLine]
    destination: Address

    class Config:
        schema_extra = {
            'example': {
                'buyer_id': str(ObjectId()),
                'lines': [OrderLine.schema()['example']],
                'destination': Address.schema()['example'],
            }
        }


class OrderCreateResponse(BaseModel):
    order_id: str

    class Config:
        schema_extra = {
            'example': {
                'order_id': str(ObjectId()),
            }
        }


class OrderStatus(str, Enum):
    waiting: str = 'waiting'
    paid: str = 'paid'
    cancelled: str = 'cancelled'


class OrderUpdateStatusResponse(BaseModel):
    order_id: str
    status: OrderStatus

    class Config:
        schema_extra = {
            'example': {
                'order_id': str(ObjectId()),
                'status': 'paid',
            }
        }

    @classmethod
    def from_order_id(cls, order_id: OrderId):
        return cls(order_id=str(order_id))


class OrderDetail(BaseModel):
    buyer_id: str
    payment_id: str
    lines: List[OrderLine]

    product_cost: float
    delivery_cost: float
    total_cost: float
    status: OrderStatus

    class Config:
        schema_extra = {
            'example': {
                'buyer_id': str(ObjectId()),
                'payment_id': str(uuid.uuid4()),
                'lines': [OrderLine.schema()['example']],
                'product_cost': 424.2,
                'delivery_cost': 42.42,
                'total_cost': 466.62,
                'status': 'waiting',
            }
        }

    @classmethod
    def from_order(cls, order: DomainOrder):
        return cls(**order.serialize(), total_cost=order.total_cost)


class HealthCheck(BaseModel):
    status: int
