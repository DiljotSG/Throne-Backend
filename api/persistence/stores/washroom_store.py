class WashroomStore:
    def __init__(
        self,
        washroom_persistence,
        review_persistence,
        amenity_persistence,
        ratings_persistence
    ):
        self.__washroom_persistence = washroom_persistence
        self.__review_persistence = review_persistence
        self.__amenity_persistence = amenity_persistence
        self.__amenity_persistence = amenity_persistence
        self.__ratings_persistence = ratings_persistence

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
            item = washroom.__dict__
            self.__transform_washroom(item.copy())
            result.append(item)

        return result

    def get_washroom(self, washroom_id):
        result = self.__washroom_persistence.get_washroom(washroom_id).__dict__
        self.__transform_washroom(result.copy())
        return result

    def get_washroom_reviews(self, washroom_id):
        result = []
        query_result = self.__review_persistence.get_reviews_for_washroom(
            washroom_id
        )

        for review in query_result:
            result.append(review.__dict__)

        return result

    def get_washrooms_by_building(self, washroom_id):
        result = []
        query_result = self.__washroom_persistence.get_washrooms_by_building(
            washroom_id
        )

        for washroom in query_result:
            item = washroom.__dict__
            self.__transform_washroom(item.copy())
            result.append(item)

        return result

    def __transform_washroom(self, washroom):
        # Expand amenities
        amenities_id = washroom.pop("amenities_id", None)
        washroom["amenities"] = self.__amenity_persistence.get_amenities(
            amenities_id
        )

        # Expand average ratings
        average_rating_id = washroom.pop("average_rating_id", None)
        item = self.__ratings_persistence.get_rating(
            average_rating_id
        ).__dict__
        item.pop("id", None)
        washroom["average_ratings"] = item
        return washroom
