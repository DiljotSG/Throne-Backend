from ...db_objects.rating import Rating
from ..interfaces.rating_interface import IRatingsPersistence


class RatingsStubPersistence(IRatingsPersistence):
    def __init__(self):
        self.ratings = []

    def add_rating(
        self,
        cleanliness,
        privacy,
        smell,
        toilet_paper_quality,
    ):
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
        rating_id
    ):
        if rating_id >= 0 and rating_id < len(self.ratings):
            return self.ratings[rating_id]
        return None

    def remove_rating(
        self,
        rating_id
    ):
        if rating_id >= 0 and rating_id < len(self.ratings):
            self.ratings.pop(rating_id)
