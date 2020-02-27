class ReviewStore:
    def __init__(
        self,
        review_persistence,
        rating_persistence,
        user_persistence
    ):
        self.__review_persistence = review_persistence
        self.__rating_persistence = rating_persistence
        self.__user_persistence = user_persistence

    def create(
        self,
        washroom_id: int,
        user_id: int,
        comment: str,
        ratings: dict
    ) -> dict:
        return None

    def update(
        self,
        washroom_id: int,
        user_id: int,
        comment: str,
        ratings: dict
    ) -> dict:
        return None

    def delete(
        self,
        review_id: int
    ) -> None:
        pass

    def get_review(self, review_id: int) -> dict:
        result = self.__review_persistence.get_review(
            review_id
        )
        if result:
            result = result.__dict__.copy()
            self.__expand_review(result)
        return result

    def __expand_review(self, review: dict):
        # Expand ratings
        rating_id = review.pop("rating_id", None)
        rating_item = self.__rating_persistence.get_rating(
            rating_id
        ).__dict__.copy()

        rating_item.pop("id", None)
        review["ratings"] = rating_item

        user_id = review.pop("user_id", None)
        user_item = self.__user_persistence.get_user(
            user_id
        ).__dict__.copy()
        user_item.pop("preference_id", None)
        user_item.pop("created_at", None)
        review["user"] = user_item
