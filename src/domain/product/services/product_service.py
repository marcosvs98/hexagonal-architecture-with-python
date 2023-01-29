from typing import List, Tuple
from abc import ABC, abstractmethod

from .product_id import ProductId
from .price_thb import PriceThb


class ProductServiceAbstract(ABC):
    @abstractmethod
    async def total_price(self, product_counts: List[Tuple[ProductId, int]]) -> PriceThb:
        pass