from . import get_sql_connection
from datetime import datetime

from api.common import convert_to_mysql_timestamp
from .favorite_impl import FavoritesPersistence
from .review_impl import ReviewsPersistence
from ...objects.user import User
from ..interfaces.user_interface import IUsersPersistence


class UsersPersistence(IUsersPersistence):
    def __init__(self):
        self.favPersistence = FavoritesPersistence()
        self.reviewPersistence = ReviewsPersistence()

    def add_user(
        self,
        username,
        profile_pic,
        preference_id  # Foreign key
    ):
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

        # Get the ID of what we just inserted
        cursor.execute(find_query)
        return list(cursor)[0][0]

    def get_user(
        self,
        user_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = """
        SELECT username, created, profilePic, preferences
        FROM users WHERE id = %s
        """
        find_tuple = (user_id,)
        cursor.execute(find_query, find_tuple)

        result = list(cursor)
        if len(result) != 1:
            return None
        result = result[0]

        return User(
            user_id, result[0], result[1], result[2], result[3]
        )

    def remove_user(
        self,
        user_id
    ):
        # Removing users is not MVP
        pass
