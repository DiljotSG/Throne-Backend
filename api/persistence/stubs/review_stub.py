from ..interfaces.review_interface import IReviewsPersistence
from ...objects.review import Review

from datetime import datetime
from typing import List, Optional


class ReviewsStubPersistence(IReviewsPersistence):
    def __init__(self) -> None:
        self.reviews: List[Review] = []

    def add_review(
        self,
        washroom_id: int,  # Foreign Key
        user_id: int,  # Foreign Key
        rating_id: int,  # Foreign Key
        comment: str,
        upvote_count: int
    ) -> int:
        review_id = len(self.reviews)
        new_review = Review(
            review_id,
            washroom_id,
            datetime.now(),
            user_id,
            comment,
            upvote_count,
            rating_id
        )
        self.reviews.append(new_review)
        # Return Review id
        return review_id

    def update_review(
        self,
        review_id: int,
        washroom_id: int,  # Foreign Key
        user_id: int,  # Foreign Key
        rating_id: int,  # Foreign Key
        comment: str,
        upvote_count: int
    ) -> Optional[Review]:
        updated_review = None
        if review_id >= 0 and review_id < len(self.reviews) and \
           self.reviews[review_id] is not None:
            updated_review = Review(
                review_id,
                washroom_id,
                datetime.now(),
                user_id,
                comment,
                upvote_count,
                rating_id
            )
            self.reviews[review_id] = updated_review
        return updated_review

    def get_review(
        self,
        review_id: int
    ) -> Optional[Review]:
        if review_id >= 0 and review_id < len(self.reviews) and\
           self.reviews[review_id] is not None:
            return self.reviews[review_id]
        return None

    def get_reviews_by_user(
        self,
        user_id: int  # Foreign Key
    ) -> List[Review]:
        user_reviews = []

        for review in self.reviews:
            if review is not None and user_id == review.id:
                user_reviews.append(review)

        return user_reviews

    def get_reviews_by_washroom(
        self,
        washroom_id: int  # Foreign Key
    ) -> List[Review]:
        washroom_reviews = []

        for review in self.reviews:
            if review is not None and washroom_id == review.washroom_id:
                washroom_reviews.append(review)

        return washroom_reviews

    def remove_review(
        self,
        review_id: int
    ) -> None:
        if review_id >= 0 and review_id < len(self.reviews):
            self.reviews.pop(review_id)
