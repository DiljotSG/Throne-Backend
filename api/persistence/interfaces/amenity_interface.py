from abc import ABC
from abc import abstractmethod


class IAmenitiesPersistence(ABC):
    @abstractmethod
    def add_amenities(
        self,
        *amenities
    ):
        # Return Amenity id
        pass

    @abstractmethod
    def get_amenities(
        self,
        amenity_id
    ):
        pass

    @abstractmethod
    def remove_amenities(
        self,
        amenity_id
    ):
        pass
