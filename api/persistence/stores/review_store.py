class ReviewStore:
    def __init__(
        self,
        review_persistence
    ):
        self.__review_persistence = review_persistence

    def get_review(self, id):
        return self.__review_persistence.get_review(id)