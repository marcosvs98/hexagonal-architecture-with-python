from domain.model.base import Entity

from .product_id import ProductId


class Product(Entity):
    product_id: ProductId
    price: float
