class ReviewStore:
    def __init__(
        self,
        review_persistence,
        rating_persistence
    ):
        self.__review_persistence = review_persistence
        self.__rating_persistence = rating_persistence

    def get_review(self, review_id):
        result = self.__review_persistence.get_review(
            review_id
        ).__dict__.copy()
        self.__transform_review(result)
        return result

    def __transform_review(self, review):
        # Expand rating
        rating_id = review.pop("rating_id", None)
        item = self.__rating_persistence.get_rating(
            rating_id
        ).__dict__.copy()
        item.pop("id", None)
        review["rating"] = item
        return review
