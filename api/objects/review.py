from datetime import datetime
from api.persistence.interfaces.rating_interface import IRatingsPersistence
from api.persistence.interfaces.user_interface import IUsersPersistence
from api.persistence.interfaces.preference_interface import \
    IPreferencesPersistence


class Review:
    def __init__(
        self,
        review_id: int,
        washroom_id: int,
        created_at: datetime,
        user_id: int,
        comment: str,
        upvote_count: int,
        rating_id: int
    ):
        self.id = review_id
        self.washroom_id = washroom_id
        self.created_at = created_at
        self.user_id = user_id
        self.comment = comment
        self.upvote_count = upvote_count
        self.rating_id = rating_id

    @staticmethod
    def verify(comment: str) -> bool:
        # TODO: Add support for verifying if a comment contains
        # valid input. Ex. is not empty, etc
        return True

    def to_dict(
        self,
        rating_persistence: IRatingsPersistence,
        user_persistence: IUsersPersistence,
        preference_persistence: IPreferencesPersistence
    ) -> dict:
        review = self.__dict__.copy()

        # Expand ratings
        rating_id = review.pop("rating_id", None)
        rating = rating_persistence.get_rating(
            rating_id
        )

        # Make mypy happy
        if rating:
            review["ratings"] = rating.to_dict()

        # Expand user
        user_id = review.pop("user_id", None)
        user = user_persistence.get_user(
            user_id
        )

        # Make mypy happy
        if user:
            review["user"] = user.to_dict(
                preference_persistence
            )

        return review
