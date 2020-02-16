from interfaces.review_interface import IReviewsPersistence


class ReviewsPersistence(IReviewsPersistence):
    def add_review(
        self,
        washroom_id,  # Foreign Key
        user_id,  # Foreign Key
        rating_id,  # Foreign Key
        comment,
        upvote_count
    ):
        # Return Review id
        pass

    def get_review(
        self,
        review_id
    ):
        pass

    def get_reviews_from_user(
        self,
        user_id  # Foreign Key
    ):
        pass

    def get_reviews_for_washroom(
        self,
        washroom_id  # Foreign Key
    ):
        pass

    def remove_review(
        self,
        review_id
    ):
        pass
