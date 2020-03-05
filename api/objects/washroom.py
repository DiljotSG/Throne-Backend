from datetime import datetime
from .location import Location


class Washroom:
    def __init__(
        self,
        washroom_id: int,
        comment: str,
        location: Location,
        created_at: datetime,
        gender: str,
        floor: int,
        urinal_count: int,
        stall_count: int,
        building_id: int,
        overall_rating: float,
        average_rating_id: int,
        amenities_id: int,
        review_count: int,
    ) -> None:
        self.id = washroom_id
        self.comment = comment
        self.location = location
        self.created_at = created_at
        self.gender = gender
        self.floor = floor
        self.urinal_count = urinal_count
        self.stall_count = stall_count
        self.building_id = building_id
        self.overall_rating = overall_rating
        self.average_rating_id = average_rating_id
        self.amenities_id = amenities_id
        self.review_count = review_count

    @staticmethod
    def verify(
        title: str
    ) -> bool:
        return len(title) > 0
