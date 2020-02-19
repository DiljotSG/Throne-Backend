class BuildingStore:
    def __init__(self, building_persistence, review_persistence):
        self.building_persistence = building_persistence
        self.review_persistence = review_persistence

    def get_building(self, id):
        return self.building_persistence.get_building(id)

    def get_buildings(
        self,
        location,
        radius,
        max_buildings,
        desired_amenities
    ):
        return self.building_persistence.query_buildings(
            location,
            radius,
            max_buildings,
            desired_amenities
        )

    def get_building_reviews(self, id):
        pass
