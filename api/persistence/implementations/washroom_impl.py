from . import get_sql_connection
from ..interfaces.washroom_interface import IWashroomsPersistence
from .amenity_impl import AmenitiesPersistence
from .review_impl import ReviewsPersistence

from ...objects.washroom import Washroom
from ...objects.location import Location
from ...objects.amenity import Amenity
from api.common import convert_to_mysql_timestamp
from api.common import distance_between_locations
from datetime import datetime
from typing import List, Optional


# The ordering of these indicies are determined by the order of properties
# returned by the queries. Look at the query or the database code and you
# can verify this for yourself.
def result_to_washroom(result):
    return Washroom(
        result[0], result[5], Location(result[3], result[4]),
        result[1], result[7], result[6], result[2], result[9],
        result[10], result[8]
    )


class WashroomsPersistence(IWashroomsPersistence):
    def __init__(self):
        self.amenitiesPersistence = AmenitiesPersistence()
        self.reviewsPersistence = ReviewsPersistence()

    def add_washroom(
        self,
        building_id: int,  # Foreign Key
        location: Location,
        title: str,
        floor: int,
        gender: str,
        amenities_id: int,  # Foreign Key
        overall_rating: int,
        average_ratings_id: int  # Foreign Key
    ) -> int:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        insert_query = """
        INSERT INTO washrooms
        (created, buildingID, latitude, longitude, title,
         floor, gender, amenities, overallRating, avgRatingsID)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (
            convert_to_mysql_timestamp(datetime.now()), building_id,
            location.latitude, location.longitude, title, floor, gender,
            amenities_id, overall_rating, average_ratings_id
        )

        # Insert and commit
        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        # Get the ID of the thing that we just inserted
        cursor.execute(find_query)
        returnid = cursor.fetchall()[0][0]

        return returnid

    def query_washrooms(
        self,
        location: Location,
        radius: float,
        max_washrooms: int,
        desired_amenities: List[Amenity]
    ) -> List[Washroom]:
        # I don't know of any way to do this complex formula in SQL, so
        # instead we're just grabbing ALL WASHROOMS AT ONCE and calculating
        # distance. It might seem inefficient but it's really not - we'd
        # have to do it either way.
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM washrooms"
        cursor.execute(find_query)

        results = cursor.fetchall()
        cnx.commit()

        results = [result_to_washroom(result) for result in results]

        if location is not None:
            # Restrict by radius
            results = [
                washroom for washroom in results
                if distance_between_locations(
                    location, washroom.location) <= radius
            ]

        # Restrict by amenities
        desired = set(desired_amenities)
        results = [
            washroom for washroom in results
            if desired.issubset(
                set(self.amenitiesPersistence.get_amenities(
                    washroom.amenities_id))
            )
        ]

        # Restrict by max results
        return results[:max_washrooms]

    def get_washrooms_by_building(
        self,
        building_id: int
    ) -> List[Washroom]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM washrooms WHERE buildingID = %s"
        find_tuple = (building_id,)

        cursor.execute(find_query, find_tuple)
        results = cursor.fetchall()
        cnx.commit()

        results = [result_to_washroom(result) for result in results]
        return results

    def get_washroom(
        self,
        washroom_id: int
    ) -> Optional[Washroom]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM washrooms WHERE id = %s"
        find_tuple = (washroom_id,)
        cursor.execute(find_query, find_tuple)
        result = cursor.fetchall()
        cnx.commit()

        if len(result) != 1:
            return None

        result = result[0]
        return result_to_washroom(result)

    def remove_washroom(
        self,
        washroom_id: int
    ) -> None:
        # Remove reviews, remove it from favorites, remove its amenities,
        # remove its avg ratings, then remove the washroom
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM washrooms WHERE id = %s"

        query0 = "SELECT id FROM reviews WHERE washroomID = %s"
        query1 = "DELETE FROM favorites WHERE washroomID = %s"
        query2 = "DELETE FROM washrooms WHERE id = %s"
        query3 = "DELETE FROM amenities WHERE id = %s"
        query4 = "DELETE FROM ratings WHERE id = %s"

        cursor.execute(find_query, (washroom_id,))
        result = result_to_washroom(list(cursor)[0])

        cursor.execute(query0, (washroom_id,))
        reviewList = cursor.fetchall()

        for review in reviewList:
            self.reviewsPersistence.remove_review(review[0])

        cursor.execute(query1, (washroom_id,))
        cursor.execute(query2, (washroom_id,))
        cursor.execute(query3, (result.amenities_id,))
        cursor.execute(query4, (result.average_rating_id,))
        cnx.commit()
