from abc import ABC
from abc import abstractmethod
from ...objects.amenity import Amenity
from ...objects.building import Building
from typing import Dict, List


class IBuildingsPersistence(ABC):
    @abstractmethod
    def add_building(
        self,
        location: Dict[str, float],
        title: str,
        map_service_id: int,
        overall_rating: int,
        best_rating_id: int
    ) -> int:
        # Return Building id
        pass

    @abstractmethod
    def query_buildings(
        self,
        location: Dict[str, float],
        radius: float,
        max_buildings: int,
        desired_amenities: List[Amenity]
    ) -> List[Building]:
        pass

    @abstractmethod
    def get_building(
        self,
        building_id: int
    ) -> Building:
        pass

    @abstractmethod
    def remove_building(
        self,
        building_id: int
    ) -> None:
        pass
