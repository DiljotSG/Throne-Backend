from typing import List, Any

from api.common import verify_gender
from ..interfaces.amenity_interface import IAmenitiesPersistence
from ..interfaces.building_interface import IBuildingsPersistence
from ..interfaces.favorite_interface import IFavoritesPersistence
from ..interfaces.preference_interface import IPreferencesPersistence
from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.user_interface import IUsersPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence
from ...exceptions.throne_unauthorized_exception import ThroneUnauthorizedException
from ...exceptions.throne_validation_exception import ThroneValidationException
from ...persistence.common import get_current_user_id


class UserStore:
    def __init__(
        self,
        user_persistence: IUsersPersistence,
        favorite_preference: IFavoritesPersistence,
        review_persistence: IReviewsPersistence,
        preference_persistence: IPreferencesPersistence,
        ratings_persistence: IRatingsPersistence,
        washroom_persistence: IWashroomsPersistence,
        building_persistence: IBuildingsPersistence,
        amenity_persistence: IAmenitiesPersistence
    ):
        self.__user_persistence: IUsersPersistence = user_persistence
        self.__favorite_persistence: IFavoritesPersistence = favorite_preference
        self.__review_persistence: IReviewsPersistence = review_persistence
        self.__preference_persistence: IPreferencesPersistence = preference_persistence
        self.__ratings_persistence: IRatingsPersistence = ratings_persistence
        self.__washroom_persistence: IWashroomsPersistence = washroom_persistence
        self.__building_persistence: IBuildingsPersistence = building_persistence
        self.__amenity_persistence: IAmenitiesPersistence = amenity_persistence

    def get_current_user(self) -> dict:
        return self.get_user(get_current_user_id(
            self.__user_persistence,
            self.__preference_persistence
        ))

    def get_user(self, user_id: int) -> dict:
        result: Any = self.__user_persistence.get_user(
            user_id
        )
        if result:
            result = result.to_dict(
                self.__preference_persistence
            )
        return result

    def get_reviews_by_user(self, user_id: int) -> List[dict]:
        result = []
        query_result = self.__review_persistence.get_reviews_by_user(user_id)

        for review in query_result:
            item = review.to_dict(
                self.__ratings_persistence,
                self.__user_persistence,
                self.__preference_persistence
            )
            result.append(item)

        return result

    def get_reviews(self) -> List[dict]:
        user_id = get_current_user_id(
            self.__user_persistence,
            self.__preference_persistence
        )
        return self.get_reviews_by_user(user_id)

    def get_favorites(self) -> List[dict]:
        result = []
        query_result = self.__favorite_persistence.get_favorites_by_user(
            get_current_user_id(
                self.__user_persistence,
                self.__preference_persistence
            )
        )

        if query_result:
            for favorite in query_result:
                item = favorite.to_dict(
                    self.__washroom_persistence,
                    self.__building_persistence,
                    self.__amenity_persistence,
                    self.__ratings_persistence,
                    self.__favorite_persistence,
                    self.__user_persistence,
                    self.__preference_persistence
                )
                self.__expand_fav_washroom(item)
                result.append(item)

        return result

    def add_favorite(
        self,
        washroom_id: int
    ) -> List[dict]:
        washroom = self.__washroom_persistence.get_washroom(washroom_id)

        if washroom is None:
            raise ThroneValidationException("Washroom id is invalid")

        user_id = get_current_user_id(
                self.__user_persistence,
                self.__preference_persistence
            )

        query_result = self.__favorite_persistence.get_favorites_by_user(
            user_id
        )

        if query_result:
            for favorite in query_result:
                if favorite.washroom_id == washroom_id:
                    return self.get_favorites()

        self.__favorite_persistence.add_favorite(
            user_id,
            washroom_id
        )

        return self.get_favorites()

    def remove_favorite(
        self,
        washroom_id: int
    ) -> bool:
        favorites = self.__favorite_persistence.get_favorites_by_user(
            get_current_user_id(
                self.__user_persistence,
                self.__preference_persistence
            )
        )

        for fav in favorites:
            if fav.washroom_id == washroom_id:
                self.__favorite_persistence.remove_favorite(fav.id)
                return True

        return False

    def update_preferences(
        self,
        gender: str,
        wheelchair_accessible: bool,
        main_floor_access: bool
    ) -> dict:
        if not verify_gender(gender):
            raise ThroneValidationException("Gender is invalid")

        user_id = get_current_user_id(
            self.__user_persistence,
            self.__preference_persistence
        )

        user = self.__user_persistence.get_user(
            user_id
        )

        if user is None:  # This is mostly for mypy
            raise ThroneUnauthorizedException()

        self.__preference_persistence.update_preference(
            user.preference_id,
            gender,
            wheelchair_accessible,
            main_floor_access
        )

        return self.get_user(user_id)

    def __expand_fav_washroom(self, item: dict):
        item["is_favorite"] = True
