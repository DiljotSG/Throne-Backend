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
            item = washroom.__dict__.copy()
            self.__transform_washroom(item)
            result.append(item)

        return result

    def get_washroom(self, washroom_id):
        result = self.__washroom_persistence.get_washroom(
            washroom_id
        )
        if result:
            result = result.__dict__.copy()
            self.__transform_washroom(result)
        return result

    def get_reviews_by_washrooms(self, washroom_id):
        result = []
        query_result = self.__review_persistence.get_reviews_by_washroom(
            washroom_id
        )

        for review in query_result:
            item = review.__dict__.copy()
            self.__transform_review(item)
            result.append(item)

        return result

    def get_washrooms_by_building(self, building_id):
        result = []
        query_result = self.__washroom_persistence.get_washrooms_by_building(
            building_id
        )

        for washroom in query_result:
            item = washroom.__dict__.copy()
            self.__transform_washroom(item)
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
        ).__dict__.copy()

        item.pop("id", None)
        washroom["average_ratings"] = item

    def __transform_review(self, review):
        # Expand ratings
        rating_id = review.pop("rating_id", None)
        item = self.__ratings_persistence.get_rating(
            rating_id
        ).__dict__.copy()

        item.pop("id", None)
        review["rating"] = item
