from abc import ABC
from abc import abstractmethod

from ...objects.review import Review
from typing import List, Optional


class IReviewsPersistence(ABC):
    @abstractmethod
    def add_review(
        self,
        washroom_id: int,  # Foreign Key
        user_id: int,  # Foreign Key
        rating_id: int,  # Foreign Key
        comment: str,
        upvote_count: int
    ) -> int:
        # Return Review id
        pass

    @abstractmethod
    def update_review(
        self,
        review_id: int,
        washroom_id: int,  # Foreign Key
        user_id: int,  # Foreign Key
        rating_id: int,  # Foreign Key
        comment: str,
        upvote_count: int
    ) -> Optional[Review]:
        pass

    @abstractmethod
    def get_review(
        self,
        review_id: int
    ) -> Optional[Review]:
        pass

    @abstractmethod
    def get_reviews_by_user(
        self,
        user_id: int  # Foreign Key
    ) -> List[Review]:
        pass

    @abstractmethod
    def get_reviews_by_washroom(
        self,
        washroom_id: int  # Foreign Key
    ) -> List[Review]:
        pass

    @abstractmethod
    def get_review_count_by_washroom(
        self,
        washroom_id: int
    ) -> int:
        pass

    @abstractmethod
    def remove_review(
        self,
        review_id: int
    ) -> None:
        pass
