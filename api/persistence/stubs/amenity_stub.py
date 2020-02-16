from interfaces.amenity_interface import IAmenitiesPersistence


class AmenitiesPersistence(IAmenitiesPersistence):
    def add_amenity(
        self,
        *amenities
    ):
        # Return Amenity id
        pass

    def get_amenity(
        self,
        amenity_id
    ):
        pass

    def remove_amenity(
        self,
        amenity_id
    ):
        pass
