class WashroomStore:
    def __init__(
        self,
        washroom_persistence,
        review_persistence
    ):
        self.__washroom_persistence = washroom_persistence
        self.__review_persistence = review_persistence

    def get_washrooms(
        self,
        location,
        radius=5,
        max_washrooms=5,
        desired_amenities=None
    ):
        result = []
        query_result = self.__washroom_persistence.query_washrooms(
            location,
            radius,
            max_washrooms,
            desired_amenities
        )

        for washroom in query_result:
            result.append(washroom.__dict__)

        return result

    def get_washroom(self, id):
        return self.__washroom_persistence.get_washroom(id).__dict__

    def get_washroom_reviews(self, id):
        return self.__review_persistence.get_reviews_for_washroom(id).__dict__

    def get_washrooms_by_building(self, id):
        return self.__washroom_persistence. \
            get_washrooms_by_building(id).__dict__
