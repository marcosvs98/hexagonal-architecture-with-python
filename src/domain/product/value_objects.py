from typing import TYPE_CHECKING, Union

from domain.base.str_id import StrIdValueObject

from domain.base.primitive_value_object import PrimitiveValueObject


class ProductId(StrIdValueObject):
    if TYPE_CHECKING:
        def __init__(self, id_: Union[str, 'ProductId']):
            super().__init__(...)



class PriceThb(PrimitiveValueObject):
    value_type = float

    @classmethod
    def _validate(cls, price):
        price = super()._validate(price)

        if price < 0:
            raise ValueError(f'Expected PriceTHB >= 0, got {price}')

        return price

    if TYPE_CHECKING:
        def __init__(self, price: Union[float, 'PriceThb']):
            super().__init__(...)