from abc import ABC
from abc import abstractmethod
from api.objects.amenity import Amenity
from typing import List, Optional


class IAmenitiesPersistence(ABC):
    @abstractmethod
    def add_amenities(
        self,
        *amenities: Amenity
    ) -> int:
        # Return Amenity id
        pass

    @abstractmethod
    def get_amenities(
        self,
        amenities_id: int
    ) -> Optional[List[Amenity]]:
        pass

    @abstractmethod
    def remove_amenities(
        self,
        amenities_id: int
    ) -> None:
        pass
