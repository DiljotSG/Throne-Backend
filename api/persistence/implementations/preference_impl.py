from typing import Optional

from . import get_sql_connection
from ..interfaces.preference_interface import IPreferencesPersistence
from ...objects.preference import Preference


# The ordering of these indicies are determined by the order of properties
# returned by the queries. Look at the query or the database code and you
# can verify this for yourself.
def _result_to_preference(result):
    return Preference(
        result[0], result[1], result[2], result[3]
    )


class PreferencesPersistence(IPreferencesPersistence):
    def __init__(self):
        pass

    def add_preference(
        self,
        gender: str,
        wheelchair_accessible: bool,
        main_floor_access: bool
    ) -> int:
        if len(gender) > 25:
            return -1

        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        insert_query = """
        INSERT INTO preferences (gender, wheelchairAccess, mainFloorAccess)
        VALUES (%s,%s,%s)
        """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (gender, wheelchair_accessible, main_floor_access)

        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        cursor.execute(find_query)
        returnid = cursor.fetchall()[0][0]

        return returnid

    def update_preference(
        self,
        preference_id: int,
        gender: str,
        wheelchair_accessible: bool,
        main_floor_access: bool
    ) -> Optional[Preference]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        update_query = """
        UPDATE preferences
        SET gender = %s,
        wheelchairAccess = %s,
        mainFloorAccess = %s
        WHERE id = %s
        """

        update_tuple = (
            gender, wheelchair_accessible, main_floor_access, preference_id
        )
        cursor.execute(update_query, update_tuple)
        cnx.commit()

        return self.get_preference(preference_id)

    def get_preference(
        self,
        preference_id: int
    ) -> Optional[Preference]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM preferences WHERE id = %s"

        find_tuple = (preference_id,)
        cursor.execute(find_query, find_tuple)
        result = cursor.fetchall()
        cnx.commit()

        if len(result) != 1:
            return None

        result = result[0]
        return _result_to_preference(result)

    def remove_preference(
        self,
        preference_id: int
    ) -> None:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        remove_query = "DELETE FROM preferences WHERE id = %s"
        remove_tuple = (preference_id,)

        cursor.execute(remove_query, remove_tuple)
        cnx.commit()
