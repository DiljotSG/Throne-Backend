from abc import ABC
from abc import abstractmethod


class IBuildingsPersistence(ABC):
    @abstractmethod
    def add_building(
        self,
        location,
        title,
        map_service_id,
        overall_rating,
        best_ratings_id
    ):
        # Return Building id
        pass

    @abstractmethod
    def query_buildings(
        self,
        location,
        radius,
        max_buildings,
        desired_amenities
    ):
        pass

    @abstractmethod
    def get_building(
        self,
        building_id
    ):
        pass

    @abstractmethod
    def remove_building(
        self,
        building_id
    ):
        pass
