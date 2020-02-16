from interfaces.building_interface import IBuildingsPersistence


class BuildingsPersistence(IBuildingsPersistence):
    def add_building(
        self,
        location,
        title,
        map_service_id,
        overall_rating,
    ):
        # Return Building id
        pass

    def query_buildings(
        self,
        location,
        radius,
        max_buildings,
        desired_amenities
    ):
        pass

    def get_building(
        self,
        building_id
    ):
        pass

    def remove_building(
        self,
        building_id
    ):
        pass
