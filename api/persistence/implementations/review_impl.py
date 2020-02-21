import mysql.connector
from handler import get_sql_connection
from datetime import datetime
from .rating_impl import RatingsPersistence
from ...objects.review import Review
from ..interfaces.review_interface import IReviewsPersistence


class ReviewsPersistence(IReviewsPersistence):
    def __init__(self):
        pass

    def add_review(
        self,
        washroom_id,  # Foreign Key
        user_id,  # Foreign Key
        rating_id,  # Foreign Key
        comment,
        upvote_count,
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        insert_query = """
                INSERT INTO reviews (created, washroomID, user, ratingID, comment, upvoteCount)
                VALUES (%s,%s,%s,%s,%s,%s)
                """

        find_query = "SELECT LAST_INSERT_ID()"
        insert_tuple = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), washroom_id, user_id,
                        rating_id, comment, upvote_count)

        # Insert and commit
        cursor.execute(insert_query, insert_tuple)
        cnx.commit()

        # Get the ID of what we just inserted
        cursor.execute(find_query)
        return list(cursor)[0][0]

    def get_review(
        self,
        review_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT created, washroomID, user, ratingID, comment, upvoteCount FROM reviews WHERE id = %s"
        find_tuple = (review_id,)
        cursor.execute(find_query, find_tuple)

        result = list(cursor)
        if len(result) != 1:
            return None
        result = result[0]
        return Review(
            review_id, result[1], result[0], result[2], result[3], result[4], result[5]
        )

    def get_reviews_from_user(
        self,
        user_id  # Foreign Key
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM reviews WHERE user = %s"
        find_tuple = (user_id,)
        cursor.execute(find_query, find_tuple)

        reviews = list(cursor)
        return [Review(result[0], result[2], result[1], result[3],
                       result[5], result[6], result[4]) for result in reviews]


    def get_reviews_for_washroom(
        self,
        washroom_id  # Foreign Key
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT * FROM reviews WHERE washroomID = %s"
        find_tuple = (washroom_id,)
        cursor.execute(find_query, find_tuple)

        reviews = list(cursor)
        return [Review(result[0], result[2], result[1], result[3],
                       result[5], result[6], result[4]) for result in reviews]

    # TODO: Check that foreign keys are removed properly
    def remove_review(
        self,
        review_id
    ):
        cnx = get_sql_connection()
        cursor = cnx.cachedCursor

        find_query = "SELECT ratingID FROM reviews WHERE id = %s"
        remove_review_query = "DELETE FROM reviews WHERE id = %s"
        remove_rating_query = "DELETE FROM ratings WHERE id = %s"
        query_tuple = (review_id,)

        cursor.execute(find_query, query_tuple)
        ratingID = list(cursor)[0][0]
        remove_rating_tuple = (ratingID,)

        try:
            cursor.execute(remove_review_query, query_tuple)
            cursor.execute(remove_rating_query, remove_rating_tuple)
            cnx.commit()
        except mysql.connector.Error:
            cnx.rollback()
