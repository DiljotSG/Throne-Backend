from . import get_sql_connection
from ...db_objects.preference import Preference
from ..interfaces.preference_interface import IPreferencesPersistence


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
        gender,
        wheelchair_accessible,
        main_floor_access
    ):
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

        # Insert and commit
        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        # Get the ID of what we just inserted
        cursor.execute(find_query)
        return list(cursor)[0][0]

    def update_preference(
        self,
        preference_id,
        gender,
        wheelchair_accessible,
        main_floor_access
    ):
        pass

    def get_preference(
        self,
        preference_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM preferences WHERE id = %s"

        find_tuple = (preference_id,)
        cursor.execute(find_query, find_tuple)

        result = list(cursor)
        if len(result) != 1:
            return None

        result = result[0]
        return _result_to_preference(result)

    def remove_preference(
        self,
        preference_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        remove_query = "DELETE FROM preferences WHERE id = %s"
        remove_tuple = (preference_id,)

        cursor.execute(remove_query, remove_tuple)
        cnx.commit()
