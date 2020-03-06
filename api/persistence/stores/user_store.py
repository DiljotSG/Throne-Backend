from ..interfaces.favorite_interface import IFavoritesPersistence
from ..interfaces.preference_interface import IPreferencesPersistence
from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence
from ..interfaces.user_interface import IUsersPersistence
from ...persistence.common import get_current_user_id
from api.common import get_cognito_user
from api.common import verify_gender
from ...exceptions.throne_validation_exception import ThroneValidationException
from ...exceptions.throne_unauthorized_exception import \
    ThroneUnauthorizedException
from typing import List, Any


class UserStore:
    def __init__(
        self,
        user_persistence: IUsersPersistence,
        favorite_preference: IFavoritesPersistence,
        review_persistence: IReviewsPersistence,
        preference_persistence: IPreferencesPersistence,
        ratings_persistence: IRatingsPersistence,
        washroom_persistence: IWashroomsPersistence
    ):
        self.__user_persistence: IUsersPersistence = user_persistence
        self.__favorite_persistence: IFavoritesPersistence = \
            favorite_preference
        self.__review_persistence: IReviewsPersistence = review_persistence
        self.__preference_persistence: IPreferencesPersistence = \
            preference_persistence
        self.__ratings_persistence: IRatingsPersistence = ratings_persistence
        self.__washroom_persistence: IWashroomsPersistence = \
            washroom_persistence

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
            result = result.__dict__.copy()
            self.__expand_user(result)
        return result

    def get_reviews_by_user(self, user_id: int) -> List[dict]:
        result = []
        query_result = self.__review_persistence.get_reviews_by_user(user_id)

        for review in query_result:
            item = review.__dict__.copy()
            self.__expand_review(item)
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
                result.append(favorite.__dict__.copy())

        return result

    def add_favorite(
        self,
        washroom_id: int
    ) -> List[dict]:
        washroom = self.__washroom_persistence.get_washroom(washroom_id)

        if washroom is None:
            raise ThroneValidationException("Washroom id is invalid")

        # Add the new favorite
        self.__favorite_persistence.add_favorite(
            get_current_user_id(
                self.__user_persistence,
                self.__preference_persistence
            ),
            washroom_id
        )

        return self.get_favorites()

    def remove_favorite(
        self,
        washroom_id: int
    ) -> None:
        favorites = self.__favorite_persistence.get_favorites_by_user(
            get_current_user_id(
                self.__user_persistence,
                self.__preference_persistence
            )
        )

        for fav in favorites:
            if fav.washroom_id == washroom_id:
                self.__favorite_persistence.remove_favorite(fav.id)
                return

        raise ThroneValidationException("Washroom id is invalid")

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

        # Get the user
        user = self.__user_persistence.get_user(
            user_id
        )

        if user is None:  # This is mostly for mypy
            raise ThroneUnauthorizedException()

        # Update it's preferences
        self.__preference_persistence.update_preference(
            user.preference_id,
            gender,
            wheelchair_accessible,
            main_floor_access
        )

        # Get the updated user
        return self.get_user(user_id)

    def __expand_user(self, user: dict) -> None:
        # Only expand preferences if the Username matches current user

        if user["username"] == get_cognito_user():
            # Expand preferences
            preference_id = user.pop("preference_id", None)
            item = self.__preference_persistence.get_preference(
                preference_id
            ).__dict__.copy()
            item.pop("id", None)
            user["preferences"] = item

        # Cleanup
        user.pop("preference_id", None)

    def __expand_review(self, review: dict) -> None:
        # Expand ratings
        rating_id = review.pop("rating_id", None)
        item = self.__ratings_persistence.get_rating(
            rating_id
        ).__dict__.copy()

        item.pop("id", None)
        review["ratings"] = item
