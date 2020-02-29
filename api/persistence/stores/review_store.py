from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.user_interface import IUsersPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence
from ..interfaces.preference_interface import IPreferencesPersistence

from ..common import get_current_user_id

from ...exceptions.throne_validation_exception import ThroneValidationException

from ...objects.rating import Rating

from typing import Optional, Any


class ReviewStore:
    def __init__(
        self,
        review_persistence: IReviewsPersistence,
        rating_persistence: IRatingsPersistence,
        user_persistence: IUsersPersistence,
        preference_persistence: IPreferencesPersistence,
        washroom_persistence: IWashroomsPersistence
    ):
        self.__review_persistence: IReviewsPersistence = review_persistence
        self.__rating_persistence: IRatingsPersistence = rating_persistence
        self.__user_persistence: IUsersPersistence = user_persistence
        self.__preference_persistence: IPreferencesPersistence = \
            preference_persistence
        self.__washroom_persistence: IWashroomsPersistence = \
            washroom_persistence

    def create_review(
        self,
        washroom_id: int,
        comment: str,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float
    ) -> Optional[dict]:
        if self.__washroom_persistence.get_washroom(washroom_id) is None:
            raise ThroneValidationException("Washroom id is not valid")

        if not len(comment) > 0:
            raise ThroneValidationException("Comment cannot be an empty string")

        if not Rating.verify(
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        ):
            raise ThroneValidationException("Ratings are invalid")

        rating_id = self.__rating_persistence.add_rating(
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        )

        review_id = self.__review_persistence.add_review(
            washroom_id,
            get_current_user_id(
                self.__user_persistence,
                self.__preference_persistence
            ),
            rating_id,
            comment,
            0
        )

        review = self.__review_persistence.get_review(review_id)

        result = review.__dict__.copy()
        self.__expand_review(result)

        return result

    def update_review(
        self,
        washroom_id: int,
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
    ) -> None:
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
