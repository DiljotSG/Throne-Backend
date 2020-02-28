from datetime import datetime

from .location import Location


class Building:
    def __init__(
        self,
        building_id: int,
        location: Location,
        title: str,
        maps_service_id: str,
        created_at: datetime,
        overall_rating: int,
        best_rating_id: int
    ):
        self.id = building_id
        self.location = location
        self.maps_service_id = maps_service_id
        self.title = title
        self.created_at = created_at
        self.overall_rating = overall_rating
        self.best_rating_id = best_rating_id
