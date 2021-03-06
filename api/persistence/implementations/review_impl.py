from datetime import datetime
from typing import List, Optional

from api.common import convert_to_mysql_timestamp
from . import get_sql_connection
from ..interfaces.review_interface import IReviewsPersistence
from ...objects.review import Review


# The ordering of these indicies are determined by the order of properties
# returned by the queries. Look at the query or the database code and you
# can verify this for yourself.
def _result_to_review(result):
    return Review(
        result[0], result[2], result[1],
        result[3], result[5], result[6], result[4]
    )


class ReviewsPersistence(IReviewsPersistence):
    def __init__(self):
        pass

    def add_review(
        self,
        washroom_id: int,  # Foreign Key
        user_id: int,  # Foreign Key
        rating_id: int,  # Foreign Key
        comment: str,
        upvote_count: int
    ) -> int:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        insert_query = """
        INSERT INTO reviews
        (created, washroomID, user, ratingID, comment, upvoteCount)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (
            convert_to_mysql_timestamp(datetime.now()),
            washroom_id, user_id, rating_id, comment, upvote_count
        )

        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        cursor.execute(find_query)
        returnid = cursor.fetchall()[0][0]

        return returnid

    def update_review(
        self,
        review_id: int,
        washroom_id: int,  # Foreign Key
        user_id: int,  # Foreign Key
        rating_id: int,  # Foreign Key
        comment: str,
        upvote_count: int
    ) -> Optional[Review]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        update_query = """
        UPDATE reviews
        SET washroomID = %s,
        user = %s,
        ratingID = %s,
        comment = %s,
        upvoteCount = %s
        WHERE id = %s
        """

        update_tuple = (
            washroom_id, user_id, rating_id, comment, upvote_count, review_id
        )
        cursor.execute(update_query, update_tuple)
        cnx.commit()

        return self.get_review(review_id)

    def get_review(
        self,
        review_id: int
    ) -> Optional[Review]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM reviews WHERE id = %s"
        find_tuple = (review_id,)
        cursor.execute(find_query, find_tuple)
        result = cursor.fetchall()
        cnx.commit()

        if len(result) != 1:
            return None

        result = result[0]
        return _result_to_review(result)

    def get_reviews_by_user(
        self,
        user_id: int  # Foreign Key
    ) -> List[Review]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM reviews WHERE user = %s"
        find_tuple = (user_id,)
        cursor.execute(find_query, find_tuple)

        reviews = cursor.fetchall()
        cnx.commit()

        return [_result_to_review(result) for result in reviews]

    def get_reviews_by_washroom(
        self,
        washroom_id: int  # Foreign Key
    ) -> List[Review]:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM reviews WHERE washroomID = %s"
        find_tuple = (washroom_id,)
        cursor.execute(find_query, find_tuple)

        reviews = cursor.fetchall()
        cnx.commit()

        return [_result_to_review(result) for result in reviews]

    def remove_reviews_by_washroom(
        self,
        washroom_id  # Foreign key
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        reviews = self.get_reviews_by_washroom(washroom_id)
        delete_query1 = "DELETE FROM ratings WHERE id = %s"
        delete_query2 = "DELETE FROM reviews WHERE washroomID = %s"

        for review in reviews:
            cursor.execute(delete_query1, (review.rating_id,))

        cursor.execute(delete_query2, (washroom_id,))
        cnx.commit()

    # TODO: Check that foreign keys are removed properly
    def remove_review(
        self,
        review_id: int
    ) -> None:
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT ratingID FROM reviews WHERE id = %s"
        remove_review_query = "DELETE FROM reviews WHERE id = %s"
        remove_rating_query = "DELETE FROM ratings WHERE id = %s"
        query_tuple = (review_id,)

        cursor.execute(find_query, query_tuple)
        ratingID = cursor.fetchall()[0][0]
        remove_rating_tuple = (ratingID,)

        cursor.execute(remove_review_query, query_tuple)
        cursor.execute(remove_rating_query, remove_rating_tuple)
        cnx.commit()
