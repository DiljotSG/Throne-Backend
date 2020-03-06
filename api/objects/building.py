from datetime import datetime
from .location import Location
from typing import Optional
from api.common import distance_between_locations
from api.persistence.interfaces.rating_interface import IRatingsPersistence


class Building:
    def __init__(
        self,
        building_id: int,
        location: Location,
        title: str,
        maps_service_id: int,
        created_at: datetime,
        overall_rating: float,
        best_ratings_id: int,
        washroom_count: int,
    ):
        self.id = building_id
        self.location = location
        self.maps_service_id = maps_service_id
        self.title = title
        self.created_at = created_at
        self.overall_rating = overall_rating
        self.best_ratings_id = best_ratings_id
        self.washroom_count = washroom_count

    @staticmethod
    def verify(floor: int) -> bool:
        return 0 < floor < 10

    def to_dict(
        self,
        rating_persistence: IRatingsPersistence,
        user_loc: Optional[Location] = None
    ) -> dict:
        building = self.__dict__.copy()

        # Expand best ratings
        best_ratings_id = building.pop("best_ratings_id", None)
        building["best_ratings"] = rating_persistence.get_rating(
            best_ratings_id
        ).to_dict()

        # Add distance to building
        if user_loc:
            building["distance"] = distance_between_locations(
                user_loc,
                building["location"]
            ) * 1000

        # Expand location
        building["location"] = building["location"].to_dict()

        return building
