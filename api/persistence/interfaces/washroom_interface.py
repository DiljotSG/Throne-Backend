from abc import ABC
from abc import abstractmethod
from ...objects.washroom import Washroom
from ...objects.amenity import Amenity
from typing import Dict, List


class IWashroomsPersistence(ABC):

    @abstractmethod
    def add_washroom(
        self,
        building_id: int,  # Foreign Key
        location: Dict[str, float],
        title: str,
        floor: int,
        gender: str,
        amenities_id: int,  # Foreign Key
        overall_rating: int,
        average_ratings_id: int  # Foreign Key
    ) -> int:
        # Return Washroom id
        pass

    @abstractmethod
    def query_washrooms(
        self,
        location: Dict[str, float],
        radius: float,
        max_washrooms: int,
        desired_amenities: List[Amenity]
    ) -> List[Washroom]:
        pass

    @abstractmethod
    def get_washrooms_by_building(
        self,
        building_id: int
    ) -> List[Washroom]:
        pass

    @abstractmethod
    def get_washroom(
        self,
        washroom_id: int
    ) -> Washroom:
        pass

    @abstractmethod
    def remove_washroom(
        self,
        washroom_id: int
    ) -> None:
        pass
