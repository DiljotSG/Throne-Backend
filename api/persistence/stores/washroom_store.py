from typing import List, Optional, Any
from api.persistence.common import get_current_user_id

from ..interfaces.amenity_interface import IAmenitiesPersistence
from ..interfaces.building_interface import IBuildingsPersistence
from ..interfaces.favorite_interface import IFavoritesPersistence
from ..interfaces.preference_interface import IPreferencesPersistence
from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.user_interface import IUsersPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence
from ...common import verify_gender
from ...exceptions.throne_validation_exception import ThroneValidationException
from ...objects.amenity import convert_to_amenities
from ...objects.amenity import verify_amenity_list
from ...objects.building import Building
from ...objects.location import Location
from ...objects.washroom import Washroom


class WashroomStore:
    def __init__(
        self,
        washroom_persistence: IWashroomsPersistence,
        review_persistence: IReviewsPersistence,
        amenity_persistence: IAmenitiesPersistence,
        ratings_persistence: IRatingsPersistence,
        user_persistence: IUsersPersistence,
        building_persistence: IBuildingsPersistence,
        favorite_persistence: IFavoritesPersistence,
        preference_persistence: IPreferencesPersistence
    ):
        self.__washroom_persistence: IWashroomsPersistence = washroom_persistence
        self.__review_persistence: IReviewsPersistence = review_persistence
        self.__amenity_persistence: IAmenitiesPersistence = amenity_persistence
        self.__ratings_persistence: IRatingsPersistence = ratings_persistence
        self.__user_persistence: IUsersPersistence = user_persistence
        self.__building_persistence: IBuildingsPersistence = building_persistence
        self.__favorite_persistence: IFavoritesPersistence = favorite_persistence
        self.__preference_persistence: IPreferencesPersistence = preference_persistence

    def create_washroom(
        self,
        comment: str,
        longitude: float,
        latitude: float,
        gender: str,
        floor: int,
        urinal_count: int,
        stall_count: int,
        building_id: int,
        amenities: list
    ) -> Optional[dict]:
        building = self.__building_persistence.get_building(building_id)

        # Check if location is correct
        if not Location.verify(latitude, longitude):
            raise ThroneValidationException("Location provided is invalid")

        # Check if washroom title is valid
        if not Washroom.verify(comment, urinal_count, stall_count):
            raise ThroneValidationException("Washroom information is invalid")

        # Check if floor is correct - Note: Really we should be storing
        # the floor of each building and comparing it against that.
        if not Building.verify(floor):
            raise ThroneValidationException("Floor number is invalid")

        # Check if gender is correct
        if not verify_gender(gender):
            raise ThroneValidationException("Gender is invalid")

        # Check if building exists
        if building is None:
            raise ThroneValidationException("Building id is invalid")

        # Check if amenities are all valid
        if not verify_amenity_list(amenities):
            raise ThroneValidationException("Amenities contain invalid types")

        gender = gender.lower()  # Ensure its lower case
        location = Location(latitude, longitude)
        new_washroom_count = building.washroom_count + 1
        overall_rating = 0
        average_rating_id = self.__ratings_persistence.add_rating(0, 0, 0, 0)
        amenities_id = self.__amenity_persistence.add_amenities(
            convert_to_amenities(amenities)
        )

        # Create the washroom
        washroom_id = self.__washroom_persistence.add_washroom(
            building_id,
            location,
            comment,
            floor,
            gender,
            urinal_count,
            stall_count,
            amenities_id,
            overall_rating,
            average_rating_id
        )

        # Update the building
        self.__building_persistence.update_building(
            building.id,
            building.location,
            building.title,
            building.maps_service_id,
            building.overall_rating,
            building.best_ratings_id,
            new_washroom_count
        )

        # Return the washroom
        washroom = self.__washroom_persistence.get_washroom(washroom_id)

        result = {}
        if washroom:
            result = washroom.to_dict(
                self.__building_persistence,
                self.__amenity_persistence,
                self.__ratings_persistence,
                self.__favorite_persistence,
                self.__user_persistence,
                self.__preference_persistence
            )

        return result

    def get_washrooms(
        self,
        location: Optional[Location],
        radius: Optional[float],
        max_washrooms: Optional[int],
        desired_amenities: Optional[List[str]]
    ) -> List[dict]:
        # Process inputs
        if radius is None:
            radius = 5
        if max_washrooms is None:
            max_washrooms = 100
        if desired_amenities is None:
            desired_amenities = []

        result = []
        query_result = self.__washroom_persistence.query_washrooms(
            location,
            radius,
            max_washrooms,
            convert_to_amenities(desired_amenities)
        )

        for washroom in query_result:
            item = washroom.to_dict(
                self.__building_persistence,
                self.__amenity_persistence,
                self.__ratings_persistence,
                self.__favorite_persistence,
                self.__user_persistence,
                self.__preference_persistence,
                location
            )
            self.expand_washroom(item)
            result.append(item)

        # Sort by distance
        result = sorted(
            result,
            key=lambda k: ("distance" not in k, k.get("distance", None))
        )
        return result

    def get_washroom(self, washroom_id: int) -> dict:
        result: Any = self.__washroom_persistence.get_washroom(
            washroom_id
        )

        if result:
            result = result.to_dict(
                self.__building_persistence,
                self.__amenity_persistence,
                self.__ratings_persistence,
                self.__favorite_persistence,
                self.__user_persistence,
                self.__preference_persistence
            )
            self.expand_washroom(result)

        return result

    def get_reviews_by_washrooms(self, washroom_id: int) -> List[dict]:
        result = []
        query_result = self.__review_persistence.get_reviews_by_washroom(
            washroom_id
        )

        for review in query_result:
            item = review.to_dict(
                self.__ratings_persistence,
                self.__user_persistence,
                self.__preference_persistence
            )
            result.append(item)

        return result

    def get_washrooms_by_building(self, building_id: int) -> List[dict]:
        result = []
        query_result = self.__washroom_persistence.get_washrooms_by_building(
            building_id
        )

        for washroom in query_result:
            item = washroom.to_dict(
                self.__building_persistence,
                self.__amenity_persistence,
                self.__ratings_persistence,
                self.__favorite_persistence,
                self.__user_persistence,
                self.__preference_persistence
            )
            self.expand_washroom(item)
            result.append(item)

        return result

    def expand_washroom(self, item):
        favorites = \
            self.__favorite_persistence.get_favorites_by_user(
                get_current_user_id(
                    self.__user_persistence,
                    self.__preference_persistence
                )
            )
        if favorites is not None:
            item["is_favorite"] = any(
                favorite.washroom_id == item["id"]
                for favorite in favorites
            )
        else:
            item["is_favorite"] = False
