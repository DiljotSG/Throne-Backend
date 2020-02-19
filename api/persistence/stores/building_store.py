class BuildingStore:
    def __init__(
        self,
        building_persistence,
        washroom_persistence,
        review_persistence
    ):
        self.__building_persistence = building_persistence
        self.__washroom_persistence = washroom_persistence
        self.__review_persistence = review_persistence

    def get_building(self, id):
        return self.__building_persistence.get_building(id)

    def get_buildings(
        self,
        location,
        radius,
        max_buildings,
        desired_amenities
    ):
        return self.__building_persistence.query_buildings(
            location,
            radius,
            max_buildings,
            desired_amenities
        )

    def get_building_reviews(self, id):
        washrooms = self.__washroom_persistence.get_washrooms_by_buiding(id)

        reviews = []
        for washroom in washrooms:
            review = self.review_persistence.get_reviews_for_washroom(
                washroom.id
            )
            reviews.append(review)

        return reviews
