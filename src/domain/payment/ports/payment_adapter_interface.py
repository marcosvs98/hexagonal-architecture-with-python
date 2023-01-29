import abc

from domain.product.value_objects import PriceThb

from domain.payment.value_objects import PaymentId


class PaymentAdapterInterface(abc.ABC):
    @abc.abstractmethod
    async def new_payment(self, total_price: PriceThb) -> PaymentId:
        raise NotImplementedError

    @abc.abstractmethod
    async def verify_payment(self, payment_id: PaymentId) -> bool:
        raise NotImplementedError
