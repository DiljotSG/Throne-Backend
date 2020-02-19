from .. interfaces.building_interface import IBuildingsPersistence
from ... objects.building import Building
from datetime import datetime


class BuildingsStubPersistence(IBuildingsPersistence):
    def __init__(self):
        self.buildings = []

    def add_building(
        self,
        location,
        title,
        map_service_id,
        overall_rating,
    ):
        building_id = len(self.buildings)
        new_building = Building(
            building_id,
            location,
            title,
            map_service_id,
            datetime.now(),
            overall_rating
        )
        # Return Building id
        self.buildings.append(new_building)
        return building_id

    def query_buildings(
        self,
        location,
        radius,
        max_buildings,
        desired_amenities
    ):
        filtered_buildings = []

        for building in self.buildings:
            if len(filtered_buildings) >= max_buildings:
                break

            filtered_buildings.append(building)

        return filtered_buildings

    def get_building(
        self,
        building_id
    ):
        if building_id >= 0 and building_id < len(self.buildings):
            return self.buildings[building_id]
        return None

    def remove_building(
        self,
        building_id
    ):
        if building_id >= 0 and building_id < len(self.buildings):
            self.buildings.pop(building_id)
