class UserStore:
    def __init__(
        self,
        user_persistence,
        favorite_preference,
        review_persistence,
        preference_persistence,
        ratings_persistence
    ):
        self.__user_persistence = user_persistence
        self.__favorite_persistence = favorite_preference
        self.__review_persistence = review_persistence
        self.__preference_persistence = preference_persistence
        self.__ratings_persistence = ratings_persistence

    def get_user(self, user_id):
        result = self.__user_persistence.get_user(
            user_id
        )
        if result:
            result = result.__dict__.copy()
            self.__transform_user(result)
        return result

    def get_reviews_by_user(self, user_id):
        result = []
        query_result = self.__review_persistence.get_reviews_by_user(user_id)

        for review in query_result:
            item = review.__dict__.copy()
            self.__transform_review(item)
            result.append(item)

        return result

    def get_favorites_by_user(self, user_id):
        result = []
        query_result = self.__favorite_persistence.get_favorites_by_user(
            user_id
        )

        for favorite in query_result:
            result.append(favorite.__dict__.copy())

        return result

    def __transform_user(self, user):
        # Expand preferences
        preference_id = user.pop("preference_id", None)
        item = self.__preference_persistence.get_preference(
            preference_id
        ).__dict__.copy()

        item.pop("id", None)
        user["preferences"] = item

    def __transform_review(self, review):
        # Expand ratings
        rating_id = review.pop("rating_id", None)
        item = self.__ratings_persistence.get_rating(
            rating_id
        ).__dict__.copy()

        item.pop("id", None)
        review["ratings"] = item
