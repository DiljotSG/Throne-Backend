from typing import Dict


class Washroom:
    def __init__(
        self,
        washroom_id: int,
        title: str,
        location: Dict[str, float],
        created_at: str,
        gender: str,
        floor: int,
        building_id: int,
        overall_rating: int,
        average_rating_id: int,
        amenities_id: int
    ) -> None:
        self.id = washroom_id
        self.title = title
        self.location = location
        self.created_at = created_at
        self.gender = gender
        self.floor = floor
        self.building_id = building_id
        self.overall_rating = overall_rating
        self.average_rating_id = average_rating_id
        self.amenities_id = amenities_id

    @staticmethod
    def verify(
        title: str,
        longitude: float,
        latitude: float,
        gender: str,
        floor: int,
    ):
        # TODO: Verify if the supplied input is valid data 
        # to be used in creating a washroom
        return True
