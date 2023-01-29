from enum import Enum
from typing import TYPE_CHECKING, Union
from domain.base.primitive_value_object import PrimitiveValueObject

from domain.base.str_id import StrIdValueObject
from domain.base.value_object import ValueObject
from domain.base.value_object_list import ValueObjectList
from domain.product.value_objects import ProductId
from domain.base.model import Attribute, AttributeSetter


class OrderAmount(PrimitiveValueObject[int]):
    value_type = int

    def __init__(self, amount: Union[int, 'OrderAmount']):
        value: int = self._validate(amount)
        super().__init__(value)

    @classmethod
    def _validate(cls, value):
        value = super()._validate(value)

        if value < 0:
            raise ValueError(f'Expected OrderAmount >= 0, got {value}')

        return value




class OrderAmount(PrimitiveValueObject[int]):
    value_type = int

    def __init__(self, amount: Union[int, 'OrderAmount']):
        value: int = self._validate(amount)
        super().__init__(value)

    @classmethod
    def _validate(cls, value):
        value = super()._validate(value)

        if value < 0:
            raise ValueError(f'Expected OrderAmount >= 0, got {value}')

        return value


class BuyerId(StrIdValueObject):
    if TYPE_CHECKING:
        def __init__(self, id_: Union[str, 'BuyerId']):
            super().__init__(...)


class OrderLine(ValueObject):
    product_id: ProductId = Attribute()
    amount: OrderAmount = Attribute()

    if TYPE_CHECKING:
        def __init__(self, *, product_id: ProductId, amount: OrderAmount):
            super().__init__()

    _product_id: ProductId = AttributeSetter()
    _amount: OrderAmount = AttributeSetter()


class OrderLineList(ValueObjectList[OrderLine]):
    value_type = OrderLine


class OrderId(StrIdValueObject):
    if TYPE_CHECKING:
        def __init__(self, id_: Union[str, 'OrderId']):
            super().__init__(...)


class OrderStatusEnum(str, Enum):
    WAITING: str = 'waiting'
    PAID: str = 'paid'
    CANCELLED: str = 'cancelled'

    @classmethod
    def has_value(cls, value):
        return value in cls._member_map_.values()


class OrderStatus(PrimitiveValueObject[str]):
    value_type = str
    Enum = OrderStatusEnum

    def is_waiting(self) -> bool:
        return self._value == OrderStatusEnum.WAITING

    def is_paid(self) -> bool:
        return self._value == OrderStatusEnum.PAID

    def is_cancelled(self) -> bool:
        return self._value == OrderStatusEnum.CANCELLED

    @classmethod
    def _validate(cls, status):
        if isinstance(status, OrderStatusEnum):
            status = status.value
        value = super()._validate(status)

        if not OrderStatusEnum.has_value(value):
            raise ValueError(f'OrderStatus named "{value}" not exists')

        return value

    if TYPE_CHECKING:
        def __init__(self, status: Union[str, 'OrderStatus']):
            super().__init__(...)
