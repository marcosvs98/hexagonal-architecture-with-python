from typing import List, Tuple

from domain.product.value_objects import ProductId, PriceThb
from domain.product.ports.product_adapter_interface import ProductAdapterInterface


class ProductAdapter(ProductAdapterInterface):
    async def total_price(self, product_counts: List[Tuple[ProductId, int]]) -> PriceThb:
        price_list = [PriceThb(15.0) * count for product, count in product_counts]
        return PriceThb(sum(price_list))
