from datetime import datetime
from ...objects.washroom import Washroom
from ..interfaces.washroom_interface import IWashroomsPersistence
from ...objects.amenity import Amenity
from ...objects.location import Location
from typing import List


class WashroomsStubPersistence(IWashroomsPersistence):
    def __init__(self):
        self.washrooms = []

    def add_washroom(
        self,
        building_id: int,  # Foreign Key
        location: Location,
        title: str,
        floor: int,
        gender: str,
        amenities_id: int,  # Foreign Key
        overall_rating: int,
        average_ratings_id: int  # Foreign Key
    ) -> int:
        washroom_id = len(self.washrooms)
        new_washroom = Washroom(
            washroom_id,
            title,
            location,
            datetime.now(),
            gender,
            floor,
            building_id,
            overall_rating,
            average_ratings_id,
            amenities_id
        )
        self.washrooms.append(new_washroom)
        # Return Washroom id
        return washroom_id

    def query_washrooms(
        self,
        location: Location,
        radius: float,
        max_washrooms: int,
        desired_amenities: List[Amenity]
    ) -> List[Washroom]:
        filtered_washrooms = []

        for washroom in self.washrooms:
            if len(filtered_washrooms) >= max_washrooms:
                break
            if washroom is not None:
                filtered_washrooms.append(washroom)

        return filtered_washrooms

    def get_washrooms_by_building(
        self,
        building_id: int
    ) -> List[Washroom]:
        washrooms = []
        for washroom in self.washrooms:
            if washroom is not None and washroom.building_id == building_id:
                washrooms.append(washroom)
        return washrooms

    def get_washroom(
        self,
        washroom_id: int
    ) -> Washroom:
        if washroom_id >= 0 and washroom_id < len(self.washrooms) and \
           self.washrooms[washroom_id] is not None:
            return self.washrooms[washroom_id]
        return None

    def remove_washroom(
        self,
        washroom_id: int
    ) -> None:
        if washroom_id >= 0 and washroom_id < len(self.washrooms):
            self.washrooms.pop(washroom_id)
