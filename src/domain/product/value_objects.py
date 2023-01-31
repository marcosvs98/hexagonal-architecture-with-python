from typing import Union

from domain.base.value_object import StrIdValueObject

# from domain.base.primitive_value_object import PrimitiveValueObject


class ProductId(StrIdValueObject):
    id: Union[str, 'ProductId']
