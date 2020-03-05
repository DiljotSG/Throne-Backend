from abc import ABC
from abc import abstractmethod

from ...objects.washroom import Washroom
from ...objects.amenity import Amenity
from ...objects.location import Location
from typing import List, Optional


class IWashroomsPersistence(ABC):

    @abstractmethod
    def add_washroom(
        self,
        building_id: int,  # Foreign Key
        location: Location,
        comment: str,
        floor: int,
        gender: str,
        urinal_count: int,
        stall_count: int,
        amenities_id: int,  # Foreign Key
        overall_rating: float,
        average_ratings_id: int  # Foreign Key
    ) -> int:
        # Return Washroom id
        pass

    @abstractmethod
    def query_washrooms(
        self,
        location: Optional[Location],
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
    ) -> Optional[Washroom]:
        pass

    @abstractmethod
    def update_washroom(
        self,
        washroom_id: int,
        comment: str,
        location: Location,
        floor: int,
        gender: str,
        urinal_count: int,
        stall_count: int,
        amenities_id: int,
        overall_rating: float,
        average_ratings_id: int,
        review_count: int
    ) -> Optional[Washroom]:
        pass

    @abstractmethod
    def remove_washroom(
        self,
        washroom_id: int
    ) -> None:
        pass
