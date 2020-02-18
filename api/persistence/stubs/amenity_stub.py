from interfaces.amenity_interface import IAmenitiesPersistence


class AmenitiesStubPersistence(IAmenitiesPersistence):
    def __init__(self):
        self.amenities = []

    def add_amenities(
        self,
        *amenities
    ):
        self.amenities.append(amenities)

    def get_amenities(
        self,
        amenities_id
    ):
        return self.amenities[amenities_id]

    def remove_amenities(
        self,
        amenities_id
    ):
        self.amenities.pop(amenities_id)
