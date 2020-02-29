from ..interfaces.building_interface import IBuildingsPersistence
from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence

from typing import List


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
        result = self.__building_persistence.get_building(
            building_id
        )
        if result:
            result = result.__dict__.copy()
            self.__expand_building(result)
        return result

    def get_buildings(
        self,
        location=None,
        radius=5,
        max_buildings=5,
        desired_amenities=[]
    ) -> List[dict]:
        result = []
        query_result = self.__building_persistence.query_buildings(
            location,
            radius,
            max_buildings,
            desired_amenities
        )

        for building in query_result:
            item = building.__dict__.copy()
            self.__expand_building(item)
            result.append(item)

        return result

    def __expand_building(self, building: dict) -> None:
        # Expand best ratings
        best_ratings_id = building.pop("best_ratings_id", None)
        item = self.__rating_persistence.get_rating(
            best_ratings_id
        ).__dict__.copy()

        # Expand location
        building["location"] = building["location"].__dict__.copy()

        item.pop("id", None)
        building["best_ratings"] = item
