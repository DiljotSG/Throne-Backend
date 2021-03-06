from datetime import datetime
from typing import List, Optional

from ..interfaces.building_interface import IBuildingsPersistence
from ...objects.amenity import Amenity
from ...objects.building import Building
from ...objects.location import Location


class BuildingsStubPersistence(IBuildingsPersistence):
    def __init__(self) -> None:
        self.buildings: List[Building] = []

    def add_building(
        self,
        location: Location,
        title: str,
        map_service_id: int,
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
            best_ratings_id,
            0
        )
        # Return Building id
        self.buildings.append(new_building)
        return building_id

    def query_buildings(
        self,
        location: Optional[Location],
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

    def update_building(
        self,
        building_id: int,
        location: Location,
        title: str,
        maps_service_id: int,
        overall_rating: float,
        best_ratings_id: int,
        washroom_count: int,
    ) -> Optional[Building]:
        new_building = None
        if 0 <= building_id < len(self.buildings) and \
                self.buildings[building_id] is not None:
            new_building = Building(
                building_id,
                location,
                title,
                maps_service_id,
                self.buildings[building_id].created_at,
                overall_rating,
                best_ratings_id,
                washroom_count
            )
            self.buildings[building_id] = new_building
        return new_building

    def remove_building(
        self,
        building_id: int
    ) -> None:
        if 0 <= building_id < len(self.buildings):
            self.buildings.pop(building_id)
