from . import get_sql_connection
from ..interfaces.favorite_interface import IFavoritesPersistence

from ...objects.favorite import Favorite
from typing import Optional, List


# The ordering of these indicies are determined by the order of properties
# returned by the queries. Look at the query or the database code and you
# can verify this for yourself.
def _result_to_favorite(result):
    return Favorite(
            result[0], result[1], result[2]
    )


class FavoritesPersistence(IFavoritesPersistence):
    def __init__(self):
        pass

    def add_favorite(
        self,
        user_id: int,  # Foreign Key
        washroom_id: int  # Foreign Key
    ) -> int:
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

    def get_favorite(
        self,
        favorite_id: int
    ) -> Optional[Favorite]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM favorites WHERE id = %s"
        find_tuple = (favorite_id,)
        cursor.execute(find_query, find_tuple)

        result = list(cursor)
        if len(result) != 1:
            return None
        result = result[0]
        return _result_to_favorite(result)

    def get_favorites_by_user(
        self,
        user_id: int  # Foreign Key
    ) -> Optional[List[Favorite]]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM favorites WHERE userID = %s"
        find_tuple = (user_id,)

        cursor.execute(find_query, find_tuple)

        results = list(cursor)

        return [_result_to_favorite(result) for result in results]

    def remove_favorite(
        self,
        favorite_id: int
    ) -> None:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        remove_query = "DELETE FROM favorites WHERE id = %s"
        remove_tuple = (favorite_id,)

        cursor.execute(remove_query, remove_tuple)
        cnx.commit()
