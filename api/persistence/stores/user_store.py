from ..interfaces.favorite_interface import IFavoritesPersistence
from ..interfaces.preference_interface import IPreferencesPersistence
from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.user_interface import IUsersPersistence
from api.common import should_use_db
from api.common import get_cognito_user

from typing import List


class UserStore:
    def __init__(
        self,
        user_persistence: IUsersPersistence,
        favorite_preference: IFavoritesPersistence,
        review_persistence: IReviewsPersistence,
        preference_persistence: IPreferencesPersistence,
        ratings_persistence: IRatingsPersistence
    ):
        self.__user_persistence: IUsersPersistence = user_persistence
        self.__favorite_persistence: IFavoritesPersistence = \
            favorite_preference
        self.__review_persistence: IReviewsPersistence = review_persistence
        self.__preference_persistence: IPreferencesPersistence = \
            preference_persistence
        self.__ratings_persistence: IRatingsPersistence = ratings_persistence

    # Gives the currently authenticated user's ID
    def __get_current_user_id(self) -> int:
        # Get the user persistence layer and the preference persistence layer
        # We are accessing the user store's private values
        # Might be considered bad, but this is the only case we need to do this

        # Default user ID for the stubs is 0
        user_id = 0

        # If we are using the DB, we can fetch user ID
        if should_use_db():

            # We can only get the username if this is the Lambda
            # If we get None back, we are not running in the Lambda
            username = get_cognito_user()

            if username:
                # Is this user in the Users table?
                user_id = self.__user_persistence.get_id_by_username(username)

                # If they don't have a user ID, we haven't
                # inserted them into the Users table yet.
                # Let's do that now
                if user_id is None:
                    # Make their preferences object first
                    pref_id = self.__preference_persistence.add_preference(
                        None,
                        None,
                        None
                    )

                    # Finally insert this user into the Users table
                    user_id = self.__user_persistence.add_user(
                        username,
                        "default",
                        pref_id
                    )

        # We did it! We got the user ID finally.
        return user_id

    def get_user(self, user_id: int) -> dict:
        result = self.__user_persistence.get_user(
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

    def get_favorites_by_user(self, user_id: int) -> List[dict]:
        result = []
        query_result = self.__favorite_persistence.get_favorites_by_user(
            user_id
        )

        for favorite in query_result:
            result.append(favorite.__dict__.copy())

        return result

    def __expand_user(self, user: dict) -> None:
        # Expand preferences
        preference_id = user.pop("preference_id", None)
        item = self.__preference_persistence.get_preference(
            preference_id
        ).__dict__.copy()

        item.pop("id", None)
        user["preferences"] = item

    def __expand_review(self, review: dict) -> None:
        # Expand ratings
        rating_id = review.pop("rating_id", None)
        item = self.__ratings_persistence.get_rating(
            rating_id
        ).__dict__.copy()

        item.pop("id", None)
        review["ratings"] = item
