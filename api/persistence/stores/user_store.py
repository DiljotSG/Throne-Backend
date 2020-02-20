class UserStore:
    def __init__(
        self,
        user_persistence,
        favorite_preference,
        review_persistence
    ):
        self.__user_persistence = user_persistence
        self.__favorite_preference = favorite_preference
        self.__review_persistence = review_persistence

    def get_user(self, user_id):
        return self.__user_persistence.get_user(user_id).__dict__

    def get_reviews_by_user(self, user_id):
        result = []
        query_result = self.__review_persistence.get_reviews_from_user(user_id)

        for review in query_result:
            result.append(review.__dict__)

        return result

    def get_user_favorites(self, user_id):
        result = []
        query_result = self.__favorite_preference.get_favorites_for_user(user_id)

        for favorite in query_result:
            result.append(favorite.__dict__)

        return result
