from datetime import datetime
from .location import Location


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
        return floor > 0 and floor < 10
