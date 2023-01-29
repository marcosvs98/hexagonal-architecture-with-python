import abc
from domain.maps.value_objects import Address, DistanceKm


class MapsAdapterInterface(abc.ABC):
    @abc.abstractmethod
    async def calculate_distance_from_warehouses(self, destination: Address) -> DistanceKm:
       raise NotImplementedError
