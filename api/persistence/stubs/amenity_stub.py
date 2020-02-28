from ..interfaces.amenity_interface import IAmenitiesPersistence
from ...objects.amenity import Amenity
from typing import List


class AmenitiesStubPersistence(IAmenitiesPersistence):
    def __init__(self):
        self.amenities = []

    def add_amenities(
        self,
        *amenities: Amenity
    ) -> int:
        self.amenities.append(amenities)
        return len(self.amenities) - 1

    def get_amenities(
        self,
        amenities_id: int
    ) -> List[Amenity]:
        if amenities_id >= 0 and amenities_id < len(self.amenities):
            return self.amenities[amenities_id]
        return None

    def remove_amenities(
        self,
        amenities_id: int
    ) -> None:
        if amenities_id >= 0 and amenities_id < len(self.amenities):
            self.amenities.pop(amenities_id)
