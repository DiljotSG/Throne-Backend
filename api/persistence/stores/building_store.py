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
        return self.__building_persistence.get_building(id).__dict__

    def get_buildings(
        self,
        location,
        radius=5,
        max_buildings=5,
        desired_amenities=None
    ):
        result = []
        query_result = self.__building_persistence.query_buildings(
            location,
            radius,
            max_buildings,
            desired_amenities
        )

        for building in query_result:
            result.append(building.__dict__)

        return result
