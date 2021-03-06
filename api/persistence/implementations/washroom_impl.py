from datetime import datetime
from typing import List, Optional

from api.common import convert_to_mysql_timestamp
from api.common import distance_between_locations
from . import get_sql_connection
from .amenity_impl import AmenitiesPersistence
from .review_impl import ReviewsPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence
from ...objects.amenity import Amenity
from ...objects.location import Location
from ...objects.washroom import Washroom


# The ordering of these indicies are determined by the order of properties
# returned by the queries. Look at the query or the database code and you
# can verify this for yourself.
def result_to_washroom(result):
    return Washroom(
        result[0], result[5], Location(result[3], result[4]),
        result[1], result[7], result[6], result[8], result[9],
        result[2], result[11], result[12], result[10], result[13]
    )


class WashroomsPersistence(IWashroomsPersistence):
    def __init__(self):
        self.amenitiesPersistence = AmenitiesPersistence()
        self.reviewsPersistence = ReviewsPersistence()

    def add_washroom(
        self,
        building_id: int,  # Foreign Key
        location: Location,
        comment: str,
        floor: int,
        gender: str,
        urinal_count: int,
        stall_count: int,
        amenities_id: int,  # Foreign Key
        overall_rating: float,
        average_ratings_id: int  # Foreign Key
    ) -> int:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        insert_query = """
        INSERT INTO washrooms
        (created, buildingID, latitude, longitude, comment,
        floor, gender, urinalCount, stallCount, amenities,
         overallRating, avgRatingsID, reviewCount)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (
            convert_to_mysql_timestamp(datetime.now()), building_id,
            location.latitude, location.longitude, comment, floor, gender,
            urinal_count, stall_count, amenities_id, overall_rating,
            average_ratings_id, 0
        )

        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        cursor.execute(find_query)
        returnid = cursor.fetchall()[0][0]

        return returnid

    def query_washrooms(
        self,
        location: Optional[Location],
        radius: float,
        max_washrooms: int,
        desired_amenities: List[Amenity]
    ) -> List[Washroom]:
        # I don't know of any way to do this complex formula in SQL, so
        # instead we're just grabbing ALL WASHROOMS AT ONCE and calculating
        # distance.
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM washrooms"
        cursor.execute(find_query)

        results = cursor.fetchall()
        cnx.commit()

        results = [result_to_washroom(result) for result in results]

        if location is not None:
            results = [
                washroom for washroom in results
                if distance_between_locations(
                    location, washroom.location) <= radius
            ]

        desired = set(desired_amenities)
        results = [
            washroom for washroom in results
            if desired.issubset(
                set(self.amenitiesPersistence.get_amenities(
                    washroom.amenities_id))
            )
        ]

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

    def update_washroom(
        self,
        washroom_id: int,
        comment: str,
        location: Location,
        floor: int,
        gender: str,
        urinal_count: int,
        stall_count: int,
        amenities_id: int,
        overall_rating: float,
        average_ratings_id: int,
        review_count: int
    ) -> Optional[Washroom]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        update_query = """
        UPDATE washrooms
        SET latitude = %s,
        longitude = %s,
        comment = %s,
        floor = %s,
        gender = %s,
        urinalCount = %s,
        stallCount = %s,
        amenities = %s,
        overallRating = %s,
        avgRatingsID = %s,
        reviewCount = %s
        WHERE id = %s
        """

        update_tuple = (
            location.latitude, location.longitude, comment, floor, gender,
            urinal_count, stall_count, amenities_id, overall_rating,
            average_ratings_id, review_count, washroom_id
        )
        cursor.execute(update_query, update_tuple)
        cnx.commit()

        return self.get_washroom(washroom_id)

    def remove_washroom(
        self,
        washroom_id: int
    ) -> None:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM washrooms WHERE id = %s"

        query0 = "SELECT id FROM reviews WHERE washroomID = %s"
        query1 = "DELETE FROM favorites WHERE washroomID = %s"
        query2 = "DELETE FROM washrooms WHERE id = %s"
        query3 = "DELETE FROM amenities WHERE id = %s"
        query4 = "DELETE FROM ratings WHERE id = %s"

        cursor.execute(find_query, (washroom_id,))
        result = result_to_washroom(cursor.fetchall()[0])

        cursor.execute(query0, (washroom_id,))
        reviewList = cursor.fetchall()

        for review in reviewList:
            self.reviewsPersistence.remove_review(review[0])

        cursor.execute(query1, (washroom_id,))
        cursor.execute(query2, (washroom_id,))
        cursor.execute(query3, (result.amenities_id,))
        cursor.execute(query4, (result.average_rating_id,))
        cnx.commit()
