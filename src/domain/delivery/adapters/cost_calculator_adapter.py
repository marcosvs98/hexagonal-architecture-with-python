from domain.maps.value_objects import Address, DistanceKm
from domain.product.value_objects import PriceThb
from domain.maps.ports.maps_adapter_interface import MapsAdapterInterface
from domain.delivery.ports.cost_calculator_interface import DeliveryCostCalculatorAdapterInterface  # noqa: E501

ORDER_PRICE_THRESHOLD = PriceThb(500.0)
FREE_DISTANCE_THRESHOLD = DistanceKm(10.0)
FREE = PriceThb(0.0)
FLAT_PRICE = PriceThb(50.0)
BASE_PRICE = PriceThb(50.0)
FREE_DISTANCE_THRESHOLD = DistanceKm(30.0)
PRICE_PER_EXTRA_DISTANCE = PriceThb(15.0)


class DeliveryCostCalculatorAdapter(DeliveryCostCalculatorAdapterInterface):

    def __init__(self, maps_service: MapsAdapterInterface):
        self.maps_service = maps_service

    async def calculate_cost(self, total_product_cost: PriceThb, destination: Address) -> PriceThb:
        if total_product_cost >= ORDER_PRICE_THRESHOLD:
            return await self._large_delivery_calculate_cost(destination)
        return await self._small_delivery_calculate_cost(destination)

    async def _large_delivery_calculate_cost(self, destination: Address) -> PriceThb:
        distance_from_warehouse = await self.maps_service.calculate_distance_from_warehouses(destination)

        if destination.bangkok_and_surrounding() or distance_from_warehouse <= FREE_DISTANCE_THRESHOLD:
            return FREE

        return FLAT_PRICE

    async def _small_delivery_calculate_cost(self, destination: Address) -> PriceThb:
        distance_from_warehouse = await self.maps_service.calculate_distance_from_warehouses(destination)

        if distance_from_warehouse <= FREE_DISTANCE_THRESHOLD:
            return BASE_PRICE

        distance_extra = distance_from_warehouse - FREE_DISTANCE_THRESHOLD
        cost_extra = PRICE_PER_EXTRA_DISTANCE * distance_extra

        return PriceThb(BASE_PRICE + cost_extra)
