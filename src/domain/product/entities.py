from typing import Dict, TYPE_CHECKING

from domain.model.base import Entity
from domain.model.base.model import Attribute, AttributeSetter

from .product_id import ProductId
from .price_thb import PriceThb


class Product(Entity):
    product_id: ProductId
    price: float
