from typing import Optional, TypeVar

from .base import Singleton


AdapterGetterType = TypeVar('AdapterGetterType')


def adapter_getter(adapter: AdapterGetterType) -> AdapterGetterType:
    if adapter:
        return adapter
    raise NotImplementedError()


def adapter_setter_value(attribute, value, adapter_name, type_, *, single_assign=False):
    if single_assign and attribute:
        raise ValueError(f'DomainRegistry.{adapter_name} is already set.')

    if isinstance(value, type_):
        return value

    raise TypeError(f'Expected {adapter_name} of type {type_.__name__}, got {type(value).__name__}')


class DomainRegistry(metaclass=Singleton):
    def __init__(self):
        from domain.model.delivery import DeliveryCostCalculator
        from domain.model.order import OrderService
        from domain.model.product import ProductServiceAbstract
        from domain.model.order import OrderRepositoryAbstract
        from domain.model.payment import PaymentServiceAbstract
        from domain.model.maps import MapsServiceAbstract
        from .base.event import DomainEventPublisher

        self._delivery_cost_calculator: Optional[DeliveryCostCalculator] = None
        self._order_service: Optional[OrderService] = None
        self._product_service: Optional[ProductServiceAbstract] = None
        self._payment_service: Optional[PaymentServiceAbstract] = None
        self._maps_service: Optional[MapsServiceAbstract] = None
        self._order_repository: Optional[OrderRepositoryAbstract] = None
        self._event_publisher: Optional[DomainEventPublisher] = None

    def reset(self):
        self._delivery_cost_calculator = None
        self._order_service = None
        self._product_service = None
        self._payment_service = None
        self._maps_service = None
        self._order_repository = None
        self._event_publisher = None

    def assign_defaults(self):
        from domain.model.delivery import DeliveryCostCalculator
        from domain.model.order import OrderService
        from domain.model.base.event import DummyEventPublisher

        self._delivery_cost_calculator = DeliveryCostCalculator()
        self._order_service = OrderService()
        self._event_publisher = DummyEventPublisher()

    @property
    def delivery_cost_calculator(self):
        return adapter_getter(self._delivery_cost_calculator)

    @delivery_cost_calculator.setter
    def delivery_cost_calculator(self, calculator):
        from domain.model.delivery import DeliveryCostCalculator
        self._delivery_cost_calculator = adapter_setter_value(self._delivery_cost_calculator, calculator,
                                                              'delivery_cost_calculator', DeliveryCostCalculator)

    @property
    def order_service(self):
        return adapter_getter(self._order_service)

    @order_service.setter
    def order_service(self, service):
        from domain.model.order import OrderService
        self.order_service = adapter_setter_value(self._order_service, service,
                                                  'order_service', OrderService)

    @property
    def product_service(self):
        return adapter_getter(self._product_service)

    @product_service.setter
    def product_service(self, service):
        from domain.model.product import ProductServiceAbstract
        self._product_service = adapter_setter_value(self._product_service, service,
                                                     'product_service', ProductServiceAbstract)

    @property
    def maps_service(self):
        return adapter_getter(self._maps_service)

    @maps_service.setter
    def maps_service(self, service):
        from domain.model.maps import MapsServiceAbstract
        self._maps_service = adapter_setter_value(self._maps_service, service,
                                                  'maps_service', MapsServiceAbstract)

    @property
    def payment_service(self):
        return adapter_getter(self._payment_service)

    @payment_service.setter
    def payment_service(self, service):
        from domain.model.payment import PaymentServiceAbstract
        self._payment_service = adapter_setter_value(self._payment_service, service,
                                                     'payment_service', PaymentServiceAbstract)

    @property
    def order_repository(self):
        return adapter_getter(self._order_repository)

    @order_repository.setter
    def order_repository(self, repository):
        from domain.model.order import OrderRepositoryAbstract
        self._order_repository = adapter_setter_value(self._order_repository, repository,
                                                      'order_repository', OrderRepositoryAbstract)

    @property
    def event_publisher(self):
        return adapter_getter(self._event_publisher)

    @event_publisher.setter
    def event_publisher(self, publisher):
        from domain.model.base.event import DomainEventPublisher
        self._event_publisher = adapter_setter_value(self._event_publisher, publisher,
                                                     'event_publisher', DomainEventPublisher)
