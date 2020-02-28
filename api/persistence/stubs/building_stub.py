from ..interfaces.building_interface import IBuildingsPersistence
from ...objects.building import Building
from ...objects.amenity import Amenity
from ...objects.location import Location

from datetime import datetime
from typing import List, Optional


class BuildingsStubPersistence(IBuildingsPersistence):
    def __init__(self) -> None:
        self.buildings: List[Building] = []

    def add_building(
        self,
        location: Location,
        title: str,
        map_service_id: str,
        overall_rating: int,
        best_ratings_id: int
    ) -> int:
        building_id = len(self.buildings)
        new_building = Building(
            building_id,
            location,
            title,
            map_service_id,
            datetime.now(),
            overall_rating,
            best_ratings_id
        )
        # Return Building id
        self.buildings.append(new_building)
        return building_id

    def query_buildings(
        self,
        location: Location,
        radius: float,
        max_buildings: int,
        desired_amenities: List[Amenity]
    ) -> List[Building]:
        filtered_buildings: List[Building] = []

        for building in self.buildings:
            if len(filtered_buildings) >= max_buildings:
                break
            if building is not None:
                filtered_buildings.append(building)

        return filtered_buildings

    def get_building(
        self,
        building_id: int
    ) -> Optional[Building]:
        if building_id >= 0 and building_id < len(self.buildings) and \
           self.buildings[building_id] is not None:
            return self.buildings[building_id]
        return None

    def remove_building(
        self,
        building_id: int
    ) -> None:
        if building_id >= 0 and building_id < len(self.buildings):
            self.buildings.pop(building_id)
