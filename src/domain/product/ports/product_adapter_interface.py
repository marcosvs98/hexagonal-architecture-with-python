import abc
from typing import List, Tuple
from domain.product.value_objects import ProductId, PriceThb


class ProductAdapterInterface(abc.ABC):
    @abc.abstractmethod
    async def total_price(self, product_counts: List[Tuple[ProductId, int]]) -> PriceThb:
        raise NotImplementedError
