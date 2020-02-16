from abc import ABC
from abc import abstractmethod


class IAmenitiesPersistence(ABC):
    @abstractmethod
    def add_amenity(
        self,
        *amenities
    ):
        # Return Amenity id
        pass

    @abstractmethod
    def get_amenity(
        self,
        amenity_id
    ):
        pass

    @abstractmethod
    def remove_amenity(
        self,
        amenity_id
    ):
        pass
