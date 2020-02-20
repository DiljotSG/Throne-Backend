from handler import get_sql_connection
from ...db_objects.rating import Rating
from ..interfaces.rating_interface import IRatingsPersistence


class RatingsPersistence(IRatingsPersistence):
    def __init__(self):
        pass

    def add_rating(
        self,
        clenliness,
        privacy,
        smell,
        toilet_paper_quality,
    ):
        cnx = get_sql_connection()
        cursor = cnx.cursor(prepared=True)

        insert_query = """
            INSERT INTO ratings (clenliness, privacy, smell, toiletPaperQuality)
            VALUES (%s,%s,%s,%s)
            """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (clenliness, privacy, smell, toilet_paper_quality)

        # Insert and commit
        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        # Get the ID of what we just inserted
        cursor.execute(find_query)
        return list(cursor)[0][0]

    def get_rating(
        self,
        rating_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cursor(prepared=True)

        find_query = "SELECT clenliness, privacy, smell, toiletPaperQuality FROM ratings WHERE id = %s"
        find_tuple = (rating_id,)
        cursor.execute(find_query, find_tuple)

        result = list(cursor)
        if len(result) != 1:
            return None
        result = result[0]
        return Rating(
            rating_id, result[0], result[1], result[2], result[3]
        )

    def remove_rating(
        self,
        rating_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cursor(prepared=True)

        remove_query = "DELETE FROM ratings WHERE id = %s"
        remove_tuple = (rating_id,)

        cursor.execute(remove_query, remove_tuple)
        cnx.commit()
