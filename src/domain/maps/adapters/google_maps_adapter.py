from domain.maps.ports.maps_adapter_interface import MapsAdapterInterface
from domain.maps.value_objects import Address, DistanceKm


class GoogleMapsAdapter(MapsAdapterInterface):
    async def calculate_distance_from_warehouses(self, destination: Address) -> DistanceKm:
        house_number = str(destination.house_number).split('/')[0]
        return DistanceKm(float(house_number))
