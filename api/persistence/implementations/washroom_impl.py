import mysql.connector

from handler import get_sql_connection
from datetime import datetime

from api.common import convert_to_mysql_timestamp, distance_between_locations
from .amenity_impl import AmenitiesPersistence
from ...objects.location import Location
from ...objects.washroom import Washroom
from ..interfaces.washroom_interface import IWashroomsPersistence


def result_to_washroom(result):
    return Washroom(
        result[0], result[5], Location(result[3], result[4]), result[1], result[7],
        result[6], result[2], result[9], result[10], result[8]
    )


class WashroomsPersistence(IWashroomsPersistence):
    def __init__(self):
        self.amenitiesPersistence = AmenitiesPersistence()

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
        INSERT INTO washrooms
        (created, buildingID, latitude, longitude, title, floor, gender, amenities, overallRating, avgRatingsID)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (
            convert_to_mysql_timestamp(datetime.now()), building_id, location.latitude,
            location.longitude, title, floor, gender, amenities_id, overall_rating, average_ratings_id
        )

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
        # I don't know of any way to do this complex formula in SQL, so
        # instead we're just grabbing ALL WASHROOMS AT ONCE and calculating distance.
        # It might seem inefficient but it's really not - we'd have to do it either way.
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM washrooms"
        cursor.execute(find_query)

        results = list(cursor)
        results = [result_to_washroom(result) for result in results]

        # Restrict by radius
        results = [
            washroom for washroom in results
            if distance_between_locations(location, washroom.location) <= radius
        ]

        # Restrict by amenities
        desired = set(desired_amenities)
        results = [
            washroom for washroom in results
            if desired.issubset(
                set(self.amenitiesPersistence.get_amenities(washroom.amenities_id))
            )
        ]

        # Restrict by max results
        return results[:max_washrooms]


    def get_washrooms_by_building(
        self,
        building_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM washrooms WHERE buildingID = %s"
        find_tuple = (building_id,)

        cursor.execute(find_query, find_tuple)

        results = list(cursor)
        results = [result_to_washroom(result) for result in results]

        return results

    def get_washroom(
        self,
        washroom_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM washrooms WHERE id = %s"
        find_tuple = (washroom_id,)
        cursor.execute(find_query, find_tuple)

        result = list(cursor)
        if len(result) != 1:
            return None
        result = result[0]
        return result_to_washroom(result)

    def remove_washroom(
        self,
        washroom_id
    ):
        # Remove reviews, remove it from favorites, remove its amenities,
        # remove its avg ratings, then remove the washroom
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM washrooms WHERE id = %s"
        query0 = "DELETE FROM reviews WHERE washroomID = %s"
        query1 = "DELETE FROM favorites WHERE washroomID = %s"
        query4 = "DELETE FROM washrooms WHERE id = %s"
        query2 = "DELETE FROM amenities WHERE id = %s"
        query3 = "DELETE FROM ratings WHERE id = %s"

        cursor.execute(find_query, (washroom_id,))
        result = result_to_washroom(list(cursor)[0])

        try:
            cursor.execute(query0, (washroom_id,))
            cursor.execute(query1, (washroom_id,))
            cursor.execute(query2, (result.amenities_id,))
            cursor.execute(query3, (result.average_rating_id,))
            cursor.execute(query4, (washroom_id,))
            cnx.commit()
        except mysql.connector.Error:
            cnx.rollback()
