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

    def get_user(self, id):
        return self.__user_persistence.get_user(id)

    def get_reviews_by_user(self, id):
        return self.__review_persistence.get_reviews_from_user(id)

    def get_user_favorites(self, id):
        return self.__favorite_preference.get_favorites_for_user(id)
