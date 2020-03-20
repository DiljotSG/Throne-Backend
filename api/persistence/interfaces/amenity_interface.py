from abc import ABC
from abc import abstractmethod
from typing import List, Optional

from ...objects.amenity import Amenity


class IAmenitiesPersistence(ABC):
    @abstractmethod
    def add_amenities(
        self,
        amenities: List[Amenity]
    ) -> int:
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
