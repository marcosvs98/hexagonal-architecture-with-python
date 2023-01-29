from domain.model.registry import DomainRegistry

from domain.maps.adapters.google_maps_adapter import GoogleMapsService
from domain.order.repository.mongo_order_repository import MongoOrderDatabaseRepository
from domain.payment.adapters.paypal_adapter import PayPalPaymentAdapter
from domain.product.adapters.product_adapter import ProductAdapter


def create_domain_registry(mongo_db):
    registry = DomainRegistry()
    registry.assign_defaults()

    registry.maps_service = GoogleMapsAdapter()
    registry.payment_service = PayPalPaymentAdapter()
    registry.product_service = ProductAdapter()
    registry.order_repository = MongoDBOrderRepository(mongo_db)

    return registry