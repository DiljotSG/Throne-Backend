from . import get_sql_connection
from ..interfaces.building_interface import IBuildingsPersistence
from .washroom_impl import WashroomsPersistence

from ...objects.building import Building
from ...objects.location import Location
from ...objects.amenity import Amenity
from api.common import convert_to_mysql_timestamp
from api.common import distance_between_locations
from datetime import datetime
from typing import List, Optional


# The ordering of these indicies are determined by the order of properties
# returned by the queries. Look at the query or the database code and you
# can verify this for yourself.
def _result_to_building(result):
    return Building(
        result[0], Location(result[2], result[3]), result[4], result[5],
        result[1], result[6], result[7]
    )


class BuildingsPersistence(IBuildingsPersistence):
    def __init__(self):
        self.washroomPersistence = WashroomsPersistence()

    def add_building(
        self,
        location: Location,
        title: str,
        map_service_id: int,
        overall_rating: float,
        best_rating_id: int
    ) -> int:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        insert_query = """
        INSERT INTO buildings
        (created, latitude, longitude, title,
         mapServiceID, overallRating, bestRatingID)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (
            convert_to_mysql_timestamp(datetime.now()), location.latitude,
            location.longitude, title, map_service_id,
            overall_rating, best_rating_id
        )

        # Insert and commit
        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        # Get the ID of the thing that we just inserted
        cursor.execute(find_query)
        returnid = cursor.fetchall()[0][0]

        return returnid

    def query_buildings(
        self,
        location: Optional[Location],
        radius: float,
        max_buildings: int,
        desired_amenities: List[Amenity]
    ) -> List[Building]:
        # TODO: Take into account amenities
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM buildings"
        cursor.execute(find_query)

        results = cursor.fetchall()
        cnx.commit()

        results = [_result_to_building(result) for result in results]

        if location is not None:
            # Restrict by radius
            results = [
                budiling for budiling in results
                if distance_between_locations(
                    location, budiling.location) <= radius
            ]

        return results[:max_buildings]

    def get_building(
        self,
        building_id: int
    ) -> Optional[Building]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM buildings WHERE id = %s"
        find_tuple = (building_id,)
        cursor.execute(find_query, find_tuple)

        result = cursor.fetchall()
        cnx.commit()

        if len(result) != 1:
            return None
        result = result[0]
        return _result_to_building(result)

    def update_building(
        self,
        building_id: int,
        location: Location,
        title: str,
        maps_service_id: int,
        overall_rating: float,
        best_ratings_id: int
    ) -> Optional[Building]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        update_query = """
        UPDATE buildings
        SET latitude = %s,
        longitude = %s,
        title = %s,
        mapServiceID = %s,
        overallRating = %s,
        bestRatingID = %s
        WHERE id = %s
        """

        update_tuple = (
            location.latitude, location.longitude, title, maps_service_id,
            overall_rating, best_ratings_id, building_id
        )
        cursor.execute(update_query, update_tuple)
        cnx.commit()

        return self.get_building(building_id)

    def remove_building(
        self,
        building_id: int
    ) -> None:
        # Remove all the washrooms, remove the buliding, remove the rating
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM buildings WHERE id = %s"
        query0 = "SELECT id FROM washrooms WHERE buildingID = %s"
        query1 = "DELETE FROM buildings WHERE id = %s"
        query2 = "DELETE FROM ratings WHERE id = %s"

        cursor.execute(find_query, (building_id,))
        result = _result_to_building(cursor.fetchall()[0])

        cursor.execute(query0, (building_id,))
        washroomIDs = cursor.fetchall()

        for id in washroomIDs:
            self.washroomPersistence.remove_washroom(id[0])

        cursor.execute(query1, (building_id,))
        cursor.execute(query2, (result.best_rating_id,))
        cnx.commit()
