from typing import TYPE_CHECKING, Union
from domain.base.value_object import StrIdValueObject


class PaymentId(StrIdValueObject):
    id: Union[str, 'PaymentId']