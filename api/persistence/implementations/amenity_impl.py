import mysql.connector
from handler import get_sql_connection
from api.db_objects import amenity
from ..interfaces.amenity_interface import IAmenitiesPersistence


class AmenitiesPersistence(IAmenitiesPersistence):
    def __init__(self):
        self.amenitylist = [
            amenity.PAPER_TOWEL,
            amenity.AIR_DRYER,
            amenity.SOAP,
            amenity.WHEELCHAIR_ACCESSIBLE,
            amenity.AUTOMATIC_SINK,
            amenity.AUTOMATIC_TOILET,
            amenity.AUTOMATIC_PAPER_TOWEL,
            amenity.AUTOMATIC_DRYER,
            amenity.SHOWER,
            amenity.URINAL,
            amenity.PAPER_SEAT_COVERS,
            amenity.HYGIENE_PRODUCTS,
            amenity.NEEDLE_DISPOSAL,
            amenity.CONTRACEPTION,
            amenity.BATHROOM_ATTENDANT,
            amenity.PERFUME_COLOGNE,
            amenity.LOTION,
        ]
        pass

    # Add a new amenity list
    def add_amenities(
        self,
        *amenities
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor
        insert_query = """
            INSERT INTO amenities
            (paperTowel, airDryer, soap, wheelChairAccess, autoSink, autoToilet,
             autoPaperTowel, autoDryer, shower, urinal, paperSeatCovers, hygieneProducts,
              needleDisposal, contraceptives, bathroomAttendant, perfume, lotion)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        find_query = "SELECT LAST_INSERT_ID()"

        # Strategy: create a list of bools, each of which is true if anything in the list matches it
        amenities = set(amenities)
        insert_tuple = tuple([a in amenities for a in self.amenitylist])
        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        # Get the ID of the thing that we just inserted
        cursor.execute(find_query)
        return list(cursor)[0][0]

    # Get amenity list by ID
    def get_amenities(
        self,
        amenities_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor
        find_query = "SELECT * FROM amenities WHERE id = %s"
        find_tuple = (amenities_id,)

        cursor.execute(find_query, find_tuple)
        result = list(cursor)
        if len(result) != 1:
            return None

        # Everything BUT the id of the result
        result = result[0][1:]

        # Create an amenities list from that
        return [self.amenitylist[i] for (i, boolean) in enumerate(result) if bool == 1]

    # Remove amenity list by ID
    def remove_amenities(
        self,
        amenities_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor
        delete_query = "DELETE FROM amenities WHERE id = %s"
        delete_tuple = (amenities_id,)

        try:
            cursor.execute(delete_query, delete_tuple)
            cnx.commit()
        except mysql.connector.Error:
            cnx.rollback()
