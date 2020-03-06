from typing import List, Optional

from ..interfaces.rating_interface import IRatingsPersistence
from ...objects.rating import Rating


class RatingsStubPersistence(IRatingsPersistence):
    def __init__(self) -> None:
        self.ratings: List[Rating] = []

    def add_rating(
        self,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float,
    ) -> int:
        rating_id = len(self.ratings)
        new_rating = Rating(
            rating_id,
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        )
        self.ratings.append(new_rating)
        # Return Rating id
        return rating_id

    def get_rating(
        self,
        rating_id: int
    ) -> Optional[Rating]:
        if rating_id >= 0 and rating_id < len(self.ratings) and \
           self.ratings[rating_id] is not None:
            return self.ratings[rating_id]
        return None

    def update_rating(
        self,
        rating_id: int,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float
    ) -> Optional[Rating]:
        new_rating = None
        if rating_id >= 0 and rating_id < len(self.ratings) and \
           self.ratings[rating_id] is not None:
            new_rating = Rating(
                rating_id,
                cleanliness,
                privacy,
                smell,
                toilet_paper_quality
            )
            self.ratings[rating_id] = new_rating
        return new_rating

    def remove_rating(
        self,
        rating_id: int
    ) -> None:
        if rating_id >= 0 and rating_id < len(self.ratings):
            self.ratings.pop(rating_id)
