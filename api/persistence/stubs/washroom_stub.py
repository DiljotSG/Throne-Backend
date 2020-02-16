from interfaces.washroom_interface import IWashroomsPersistence


class WashroomsPersistence(IWashroomsPersistence):

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

    def query_washrooms(
        self,
        location,
        radius,
        max_washrooms,
        desired_amenities
    ):
        pass

    def get_washroom(
        self,
        washroom_id
    ):
        pass

    def remove_washroom(
        self,
        washroom_id
    ):
        pass
