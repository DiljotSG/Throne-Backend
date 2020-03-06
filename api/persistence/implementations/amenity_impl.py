from typing import List, Optional

from . import get_sql_connection
from ..interfaces.amenity_interface import IAmenitiesPersistence
from ...objects.amenity import Amenity


class AmenitiesPersistence(IAmenitiesPersistence):
    def __init__(self):
        self.amenitylist = [e.value for e in Amenity]

    # Add a new amenity list
    def add_amenities(
        self,
        amenities: List[Amenity]
    ) -> int:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor
        insert_query = """
        INSERT INTO amenities VALUES
        (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        find_query = "SELECT LAST_INSERT_ID()"

        # Strategy: create a list of bools, each of which
        # is true if anything in the list matches it
        amenities_set: set = set(amenities)
        insert_tuple = tuple([a in amenities_set for a in self.amenitylist])
        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        # Get the ID of the thing that we just inserted
        cursor.execute(find_query)
        returnid = cursor.fetchall()[0][0]

        return returnid

    # Get amenity list by ID
    def get_amenities(
        self,
        amenities_id: int
    ) -> Optional[List[Amenity]]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor
        find_query = "SELECT * FROM amenities WHERE id = %s"
        find_tuple = (amenities_id,)

        cursor.execute(find_query, find_tuple)

        result = cursor.fetchall()
        cnx.commit()

        if len(result) != 1:
            return None

        # Everything BUT the id of the result
        result = result[0][1:]

        # Create an amenities list from that
        return [self.amenitylist[i] for (i, hasAmenity)
                in enumerate(result) if hasAmenity == 1]

    # Remove amenity list by ID
    def remove_amenities(
        self,
        amenities_id: int
    ) -> None:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        delete_query = "DELETE FROM amenities WHERE id = %s"
        delete_tuple = (amenities_id,)

        cursor.execute(delete_query, delete_tuple)
        cnx.commit()
