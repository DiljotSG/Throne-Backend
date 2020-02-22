import mysql.connector

from handler import get_sql_connection
from datetime import datetime

from ...objects.washroom import Washroom
from ..interfaces.washroom_interface import IWashroomsPersistence


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
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        insert_query = """
        INSERT INTO favorites (userID, washroomID)
        VALUES (%s,%s)
        """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (user_id, washroom_id)

        # Insert and commit
        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        # Get the ID of what we just inserted
        cursor.execute(find_query)
        return list(cursor)[0][0]

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
            if washroom is not None:
                filtered_washrooms.append(washroom)

        return filtered_washrooms

    def get_washrooms_by_building(
        self,
        building_id
    ):
        washrooms = []
        for washroom in self.washrooms:
            if washroom is not None and washroom.building_id == building_id:
                washrooms.append(washroom)
        return washrooms

    def get_washroom(
        self,
        washroom_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT userID, washroomID FROM favorites WHERE id = %s"
        find_tuple = (favorite_id,)
        cursor.execute(find_query, find_tuple)

        result = list(cursor)
        if len(result) != 1:
            return None
        result = result[0]
        return Favorite(
            favorite_id, result[0], result[1]
        )

    def remove_washroom(
        self,
        washroom_id
    ):
        # Remove reviews, remove it from favorites, then remove the washroom
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        remove_query = "DELETE FROM favorites WHERE id = %s"
        remove_tuple = (favorite_id,)

        try:
            cursor.execute(remove_query, remove_tuple)
            cnx.commit()
        except mysql.connector.Error:
            cnx.rollback()
