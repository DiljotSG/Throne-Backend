from abc import ABC
from abc import abstractmethod
from typing import List, Optional

from ...objects.amenity import Amenity
from ...objects.building import Building
from ...objects.location import Location


class IBuildingsPersistence(ABC):
    @abstractmethod
    def add_building(
        self,
        location: Location,
        title: str,
        map_service_id: str,
        overall_rating: int,
        best_rating_id: int
    ) -> int:
        # Return Building id
        pass

    @abstractmethod
    def query_buildings(
        self,
        location: Location,
        radius: float,
        max_buildings: int,
        desired_amenities: List[Amenity]
    ) -> List[Building]:
        pass

    @abstractmethod
    def get_building(
        self,
        building_id: int
    ) -> Optional[Building]:
        pass

    @abstractmethod
    def remove_building(
        self,
        building_id: int
    ) -> None:
        pass
