from abc import ABC
from abc import abstractmethod


class IWashroomsPersistence(ABC):

    @abstractmethod
    def add_washroom(
        self,
        building_id,  # Foreign Key
        location,
        title,
        floor,
        gender,
        amenities_id,  # Foreign Key
        overall_rating,
        average_ratings_id  # Foreign Key
    ):
        # Return Washroom id
        pass

    @abstractmethod
    def query_washrooms(
        self,
        location,
        radius,
        max_washrooms,
        desired_amenities
    ):
        pass

    @abstractmethod
    def get_washroom(
        self,
        washroom_id
    ):
        pass

    @abstractmethod
    def remove_washroom(
        self,
        washroom_id
    ):
        pass
