from . import get_sql_connection
from ...db_objects.preference import Preference
from ..interfaces.preference_interface import IPreferencesPersistence


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

    def get_preference(
        self,
        preference_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = """
        SELECT gender, wheelchairAccess, mainFloorAccess
        FROM preferences WHERE id = %s
        """
        find_tuple = (preference_id,)
        cursor.execute(find_query, find_tuple)

        result = list(cursor)
        if len(result) != 1:
            return None
        result = result[0]
        return Preference(
            preference_id, result[0], result[1], result[2]
        )

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
