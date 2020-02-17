from interfaces.washroom_interface import IWashroomsPersistence
from ... objects.washroom import Washroom
from datetime import datetime


class WashroomsPersistence(IWashroomsPersistence):
    def __init__(self):
        self.washrooms = []

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
        washroom_id = len(self.washrooms)
        new_washroom = Washroom(washroom_id,
                                title,
                                location,
                                datetime.now(),
                                gender,
                                floor,
                                building_id,
                                overall_rating,
                                average_ratings_id)
        self.washrooms.append(new_washroom)
        # Return Washroom id
        return washroom_id

    def query_washrooms(
        self,
        location,
        radius,
        max_washrooms,
        desired_amenities
    ):
        filtered_washrooms = []

        for washroom in self.washrooms:
            if len(filtered_washrooms) >= max_washrooms:
                break

            filtered_washrooms.append(washroom)

        return filtered_washrooms

    def get_washroom(
        self,
        washroom_id
    ):
        return self.washrooms[washroom_id]

    def remove_washroom(
        self,
        washroom_id
    ):
        self.washrooms.pop(washroom_id)
