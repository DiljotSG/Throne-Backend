from interfaces.amenity_interface import IAmenitiesPersistence


class AmenitiesPersistence(IAmenitiesPersistence):
    def __init__(self):
        self.amenities = []

    def add_amenities(
        self,
        *amenities
    ):
        self.amenities.append(amenities)

    def get_amenities(
        self,
        amenity_id
    ):
        return self.amenities[amenity_id]

    def remove_amenities(
        self,
        amenity_id
    ):
        self.amenities.pop(amenity_id)
