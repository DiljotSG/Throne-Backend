from datetime import datetime
from typing import Optional

from api.common import distance_between_locations
from api.persistence.interfaces.amenity_interface import IAmenitiesPersistence
from api.persistence.interfaces.building_interface import IBuildingsPersistence
from api.persistence.interfaces.favorite_interface import IFavoritesPersistence
from api.persistence.interfaces.preference_interface import IPreferencesPersistence
from api.persistence.interfaces.rating_interface import IRatingsPersistence
from api.persistence.interfaces.user_interface import IUsersPersistence
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

    def to_dict(
        self,
        building_persistence: IBuildingsPersistence,
        amenity_persistence: IAmenitiesPersistence,
        ratings_persistence: IRatingsPersistence,
        favorite_persistence: IFavoritesPersistence,
        user_persistence: IUsersPersistence,
        preference_persistence: IPreferencesPersistence,
        user_loc: Optional[Location] = None
    ) -> dict:
        washroom = self.__dict__.copy()

        building = building_persistence.get_building(
            washroom["building_id"]
        )
        if building is not None:
            washroom["building_title"] = building.title

        amenities_id = washroom.pop("amenities_id", None)
        washroom["amenities"] = amenity_persistence.get_amenities(
            amenities_id
        )

        if user_loc:
            washroom["distance"] = distance_between_locations(
                user_loc,
                washroom["location"]
            )

        washroom["location"] = washroom["location"].to_dict()

        average_rating_id = washroom.pop("average_rating_id", None)
        item = ratings_persistence.get_rating(
            average_rating_id
        )

        if item:
            rating = item.to_dict()
            rating.pop("id", None)
            washroom["average_ratings"] = rating

        return washroom

    @staticmethod
    def verify(
        comment: str,
        urinal_count: int,
        stall_count: int
    ) -> bool:
        return urinal_count >= 0 and stall_count >= 0
