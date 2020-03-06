from ..interfaces.building_interface import IBuildingsPersistence
from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence

from ...objects.location import Location
from ...objects.amenity import convert_to_amenities
from api.common import distance_between_locations

from typing import List, Optional, Any


class BuildingStore:
    def __init__(
        self,
        building_persistence: IBuildingsPersistence,
        washroom_persistence: IWashroomsPersistence,
        review_persistence: IReviewsPersistence,
        rating_persistence: IRatingsPersistence
    ):
        self.__building_persistence: IBuildingsPersistence = \
            building_persistence
        self.__washroom_persistence: IWashroomsPersistence = \
            washroom_persistence
        self.__review_persistence: IReviewsPersistence = review_persistence
        self.__rating_persistence: IRatingsPersistence = rating_persistence

    def get_building(self, building_id: int) -> dict:
        result: Any = self.__building_persistence.get_building(
            building_id
        )
        if result:
            result = result.to_dict(
                self.__rating_persistence
            )
        return result

    def get_buildings(
        self,
        location: Optional[Location],
        radius: Optional[float],
        max_buildings: Optional[int],
        desired_amenities: Optional[List[str]]
    ) -> List[dict]:
        # Process inputs
        if radius is None:
            radius = 5
        if max_buildings is None:
            max_buildings = 100
        if desired_amenities is None:
            desired_amenities = []

        result = []
        query_result = self.__building_persistence.query_buildings(
            location,
            radius,
            max_buildings,
            convert_to_amenities(desired_amenities)
        )

        for building in query_result:
            item = building.to_dict(
                self.__rating_persistence,
                location
            )
            result.append(item)

        # Sort by distance
        result = sorted(
            result,
            key=lambda k: ("distance" not in k, k.get("distance", None))
        )
        return result
