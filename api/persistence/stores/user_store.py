class UserStore:
    def __init__(
        self,
        user_persistence,
        favorite_preference,
        review_persistence,
        preference_persistence
    ):
        self.__user_persistence = user_persistence
        self.__favorite_persistence = favorite_preference
        self.__review_persistence = review_persistence
        self.__preference_persistence = preference_persistence

    def get_user(self, user_id):
        result = self.__user_persistence.get_user(
            user_id
        ).__dict__.copy()
        self.__transform_user(result)
        return result

    def get_reviews_by_user(self, user_id):
        result = []
        query_result = self.__review_persistence.get_reviews_from_user(user_id)

        for review in query_result:
            result.append(review.__dict__.copy())

        return result

    def get_user_favorites(self, user_id):
        result = []
        query_result = self.__favorite_persistence.get_favorites_for_user(
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
