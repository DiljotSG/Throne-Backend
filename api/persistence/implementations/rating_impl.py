from . import get_sql_connection
from ...objects.rating import Rating
from ..interfaces.rating_interface import IRatingsPersistence
from typing import Optional


# The ordering of these indicies are determined by the order of properties
# returned by the queries. Look at the query or the database code and you
# can verify this for yourself.
def _result_to_rating(result):
    return Rating(
        result[0], result[1], result[2], result[3], result[4]
    )


class RatingsPersistence(IRatingsPersistence):
    def __init__(self):
        pass

    def add_rating(
        self,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float,
    ) -> int:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        insert_query = """
        INSERT INTO ratings
        (cleanliness, privacy, smell, toiletPaperQuality)
        VALUES (%s,%s,%s,%s)
        """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (cleanliness, privacy, smell, toilet_paper_quality)

        # Insert and commit
        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        # Get the ID of what we just inserted
        cursor.execute(find_query)
        return list(cursor)[0][0]

    def get_rating(
        self,
        rating_id: int
    ) -> Optional[Rating]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM ratings WHERE id = %s"

        find_tuple = (rating_id,)
        cursor.execute(find_query, find_tuple)

        result = list(cursor)
        if len(result) != 1:
            return None
        result = result[0]
        return _result_to_rating(result)

    def update_rating(
        self,
        rating_id: int,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float
    ) -> Optional[Rating]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        update_query = """
        UPDATE ratings
        SET cleanliness = %s,
        privacy = %s,
        smell = %s,
        toiletPaperQuality = %s
        WHERE id = %s
        """

        update_tuple = (
            cleanliness, privacy, smell, toilet_paper_quality, rating_id
        )
        cursor.execute(update_query, update_tuple)
        cnx.commit()

        return self.get_rating(rating_id)

    def remove_rating(
        self,
        rating_id: int
    ) -> None:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        remove_query = "DELETE FROM ratings WHERE id = %s"
        remove_tuple = (rating_id,)

        cursor.execute(remove_query, remove_tuple)
        cnx.commit()
