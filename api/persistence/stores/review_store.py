from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.user_interface import IUsersPersistence

from typing import Optional, Any


class ReviewStore:
    def __init__(
        self,
        review_persistence: IReviewsPersistence,
        rating_persistence: IRatingsPersistence,
        user_persistence: IUsersPersistence
    ):
        self.__review_persistence: IReviewsPersistence = review_persistence
        self.__rating_persistence: IRatingsPersistence = rating_persistence
        self.__user_persistence: IUsersPersistence = user_persistence

    def create_review(
        self,
        washroom_id: int,
        user_id: int,
        comment: str,
        ratings: dict
    ) -> Optional[dict]:
        # TODO: Add support for creating a new Review based
        # on the provided data - If data is invalid, throw
        # and exception
        return None

    def update_review(
        self,
        washroom_id: int,
        user_id: int,
        comment: str,
        ratings: dict
    ) -> Optional[dict]:
        # TODO: Add support for updating a Review based
        # on the provided data - If data is invalid, throw
        # and exception
        return None

    def delete_review(
        self,
        review_id: int
    ) -> Optional[None]:
        # TODO: Add support for deleting a Review based
        # on the provided data - If data is invalid, throw
        # and exception
        pass

    def get_review(self, review_id: int) -> dict:
        result: Any = self.__review_persistence.get_review(
            review_id
        )
        if result:
            result = result.__dict__.copy()
            self.__expand_review(result)
        return result

    def __expand_review(self, review: dict) -> None:
        # Expand ratings
        rating_id = review.pop("rating_id", None)
        rating_item = self.__rating_persistence.get_rating(
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
