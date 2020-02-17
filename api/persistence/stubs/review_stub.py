from interfaces.review_interface import IReviewsPersistence
from ... objects.review import Review
from datetime import datetime


class ReviewsPersistence(IReviewsPersistence):
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
        new_review = Review(review_id,
                            washroom_id,
                            datetime.now(),
                            comment,
                            upvote_count)
        self.reviews.append(new_review)
        # Return Review id
        return review_id

    def get_review(
        self,
        review_id
    ):
        return self.reviews[review_id]

    def get_reviews_from_user(
        self,
        user_id  # Foreign Key
    ):
        user_reviews = []

        for review in self.reviews:
            if user_id == review.user_id:
                user_reviews.append(review)

        return user_reviews

    def get_reviews_for_washroom(
        self,
        washroom_id  # Foreign Key
    ):
        washroom_reviews = []

        for review in self.reviews:
            if washroom_id == review.washroom_id:
                washroom_reviews.append(review)

        return washroom_reviews

    def remove_review(
        self,
        review_id
    ):
        self.review.pop(review_id)