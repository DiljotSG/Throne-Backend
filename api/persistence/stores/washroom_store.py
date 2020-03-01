from ..interfaces.amenity_interface import IAmenitiesPersistence
from ..interfaces.favorite_interface import IFavoritesPersistence
from ..interfaces.preference_interface import IPreferencesPersistence
from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.user_interface import IUsersPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence
from ..interfaces.building_interface import IBuildingsPersistence

from ...exceptions.throne_validation_exception import ThroneValidationException

from ...objects.location import Location
from ...objects.building import Building
from ...objects.washroom import Washroom

from ...objects.amenity import verify_amenity_list
from ...objects.amenity import convert_to_amenities

from ...common import verify_gender
from api.persistence.common import get_current_user_id

from typing import List, Optional, Any


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
        self.__washroom_persistence: IWashroomsPersistence = \
            washroom_persistence
        self.__review_persistence: IReviewsPersistence = review_persistence
        self.__amenity_persistence: IAmenitiesPersistence = amenity_persistence
        self.__ratings_persistence: IRatingsPersistence = ratings_persistence
        self.__user_persistence: IUsersPersistence = user_persistence
        self.__building_persistence: IBuildingsPersistence = \
            building_persistence
        self.__favorite_persistence: \
            IFavoritesPersistence = favorite_persistence
        self.__preference_persistence: \
            IPreferencesPersistence = preference_persistence

    def create_washroom(
        self,
        title: str,
        longitude: float,
        latitude: float,
        gender: str,
        floor: int,
        building_id: int,
        amenities: list
    ) -> Optional[dict]:
        # Check if location is correct
        if not Location.verify(latitude, longitude):
            raise ThroneValidationException("Location provided is not valid")

        # Check if washroom title is valid
        if not Washroom.verify(title):
            raise ThroneValidationException("Washroom title is not valid")

        # Check if floor is correct - Note: Really we should be storing
        # the floor of each building and comparing it against that.
        if not Building.verify(floor):
            raise ThroneValidationException("Floor number is not valid")

        # Check if gender is correct
        if not verify_gender(gender):
            raise ThroneValidationException("Gender is not valid")

        # Check if building exists
        if self.__building_persistence.get_building(building_id) is None:
            raise ThroneValidationException("Building id is not valid")

        # Check if amenities are all valid
        if not verify_amenity_list(amenities):
            raise ThroneValidationException("Amenities contain invalid types")

        gender = gender.lower()  # Ensure its lower case
        location = Location(latitude, longitude)
        overall_rating_id = self.__ratings_persistence.add_rating(0, 0, 0, 0)
        average_rating_id = self.__ratings_persistence.add_rating(0, 0, 0, 0)
        amenities_id = self.__amenity_persistence.add_amenities(
            convert_to_amenities(amenities)
        )

        # Create the washroom
        washroom_id = self.__washroom_persistence.add_washroom(
            building_id,
            location,
            title,
            floor,
            gender,
            amenities_id,
            overall_rating_id,
            average_rating_id
        )

        # Return the washroom
        washroom = self.__washroom_persistence.get_washroom(washroom_id)
        item = washroom.__dict__.copy()
        self.__expand_washroom(item)

        return item

    def get_washrooms(
        self,
        location=None,
        radius=5,
        max_washrooms=5,
        desired_amenities=[]
    ) -> List[dict]:
        result = []
        query_result = self.__washroom_persistence.query_washrooms(
            location,
            radius,
            max_washrooms,
            desired_amenities
        )

        for washroom in query_result:
            item = washroom.__dict__.copy()
            self.__expand_washroom(item)
            result.append(item)

        return result

    def get_washroom(self, washroom_id: int) -> dict:
        result: Any = self.__washroom_persistence.get_washroom(
            washroom_id
        )
        if result:
            result = result.__dict__.copy()
            self.__expand_washroom(result)
        return result

    def get_reviews_by_washrooms(self, washroom_id: int) -> List[dict]:
        result = []
        query_result = self.__review_persistence.get_reviews_by_washroom(
            washroom_id
        )

        for review in query_result:
            item = review.__dict__.copy()
            self.__expand_review(item)
            result.append(item)

        return result

    def get_washrooms_by_building(self, building_id: int) -> List[dict]:
        result = []
        query_result = self.__washroom_persistence.get_washrooms_by_building(
            building_id
        )

        for washroom in query_result:
            item = washroom.__dict__.copy()
            self.__expand_washroom(item)
            result.append(item)

        return result

    def __expand_washroom(self, washroom: dict) -> None:
        # Expand amenities
        amenities_id = washroom.pop("amenities_id", None)
        washroom["amenities"] = self.__amenity_persistence.get_amenities(
            amenities_id
        )

        # Expand location
        washroom["location"] = washroom["location"].__dict__.copy()

        # Expand average ratings
        average_rating_id = washroom.pop("average_rating_id", None)
        item = self.__ratings_persistence.get_rating(
            average_rating_id
        ).__dict__.copy()

        item.pop("id", None)
        washroom["average_ratings"] = item

        # Add review count
        washroom["review_count"] = \
            self.__review_persistence.get_review_count_by_washroom(
                washroom["id"]
            )

        # Add is_favorite
        favorites = \
            self.__favorite_persistence.get_favorites_by_user(
                get_current_user_id(
                    self.__user_persistence,
                    self.__preference_persistence
                )
            )

        if favorites is not None:
            washroom["is_favorite"] = any(
                favorite.washroom_id == washroom["id"]
                for favorite in favorites
            )
        else:
            washroom["is_favorite"] = False

    def __expand_review(self, review: dict) -> None:
        # Expand ratings
        rating_id = review.pop("rating_id", None)
        rating_item = self.__ratings_persistence.get_rating(
            rating_id
        ).__dict__.copy()

        rating_item.pop("id", None)
        review["ratings"] = rating_item

        user_id = review.pop("user_id", None)
        user_item = self.__user_persistence.get_user(
            user_id
        ).__dict__.copy()
        user_item.pop("preference_id", None)
        user_item.pop("created_at", None)
        review["user"] = user_item
