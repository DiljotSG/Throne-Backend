from abc import ABC
from abc import abstractmethod


class IReviewsPersistence(ABC):
    @abstractmethod
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

    @abstractmethod
    def update_review(
        self,
        review_id,
        comment,
        upvote_count
    ):
        # this assumes ratings would be updated directly
        pass

    @abstractmethod
    def get_review(
        self,
        review_id
    ):
        pass

    @abstractmethod
    def get_reviews_by_user(
        self,
        user_id  # Foreign Key
    ):
        pass

    @abstractmethod
    def get_reviews_by_washroom(
        self,
        washroom_id  # Foreign Key
    ):
        pass

    @abstractmethod
    def remove_review(
        self,
        review_id
    ):
        pass
