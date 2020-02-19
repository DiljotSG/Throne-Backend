from datetime import datetime

from ...objects.review import Review
from ..interfaces.review_interface import IReviewsPersistence


class ReviewsStubPersistence(IReviewsPersistence):
    def __init__(self):
        self.reviews = []

    def add_review(
        self,
        washroom_id,  # Foreign Key
        user_id,  # Foreign Key
        rating_id,  # Foreign Key
        comment,
        upvote_count
    ):
        review_id = len(self.reviews)
        new_review = Review(
            review_id,
            washroom_id,
            datetime.now(),
            comment,
            upvote_count
        )
        self.reviews.append(new_review)
        # Return Review id
        return review_id

    def get_review(
        self,
        review_id
    ):
        if review_id >= 0 and review_id < len(self.reviews) and\
           self.reviews[review_id] is not None:
            return self.reviews[review_id].__dict__
        return None

    def get_reviews_from_user(
        self,
        user_id  # Foreign Key
    ):
        user_reviews = []

        for review in self.reviews:
            if user_id == review.user_id and review is not None:
                user_reviews.append(review.__dict__)

        return user_reviews

    def get_reviews_for_washroom(
        self,
        washroom_id  # Foreign Key
    ):
        washroom_reviews = []

        for review in self.reviews:
            if washroom_id == review.washroom_id and review is not None:
                washroom_reviews.append(review.__dict__)

        return washroom_reviews

    def remove_review(
        self,
        review_id
    ):
        if review_id >= 0 and review_id < len(self.reviews):
            self.review.pop(review_id)
