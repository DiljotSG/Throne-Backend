from . import get_sql_connection
from ..interfaces.user_interface import IUsersPersistence
from .favorite_impl import FavoritesPersistence
from .review_impl import ReviewsPersistence

from ...objects.user import User
from api.common import convert_to_mysql_timestamp
from datetime import datetime
from typing import Optional


# The ordering of these indicies are determined by the order of properties
# returned by the queries. Look at the query or the database code and you
# can verify this for yourself.
def _result_to_user(result):
    return User(
        result[0], result[1], result[2], result[3], result[4]
    )


class UsersPersistence(IUsersPersistence):
    def __init__(self):
        self.favPersistence = FavoritesPersistence()
        self.reviewPersistence = ReviewsPersistence()

    def add_user(
        self,
        username: str,
        profile_pic: str,
        preference_id: int  # Foreign key
    ) -> int:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        insert_query = """
        INSERT INTO users (username, created, profilePic, preferences)
        VALUES (%s,%s,%s,%s)
        """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (username, convert_to_mysql_timestamp(datetime.now()),
                        profile_pic, preference_id)

        # Insert and commit
        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        # Get the ID of the thing that we just inserted
        cursor.execute(find_query)
        returnid = cursor.fetchall()[0][0]

        return returnid

    def get_user(
        self,
        user_id: int
    ) -> Optional[User]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM users WHERE id = %s"
        find_tuple = (user_id,)
        cursor.execute(find_query, find_tuple)
        result = cursor.fetchall()
        cnx.commit()

        if len(result) != 1:
            return None

        result = result[0]
        return _result_to_user(result)

    def get_id_by_username(
        self,
        username: str
    ) -> Optional[int]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT id FROM users WHERE username = %s"
        find_tuple = (username,)
        cursor.execute(find_query, find_tuple)

        result = cursor.fetchall()
        cnx.commit()

        if len(result) != 1:
            return None

        result = result[0]
        return result[0]

    def remove_user(
        self,
        user_id: int
    ) -> None:
        # Removing users is not MVP
        pass
