from typing import TYPE_CHECKING, Union
from domain.base.str_id import StrIdValueObject


class PaymentId(StrIdValueObject):
    if TYPE_CHECKING:
        def __init__(self, payment_id: Union[str, 'PaymentId']):
            super().__init__(...)