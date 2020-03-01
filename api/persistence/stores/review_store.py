from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.user_interface import IUsersPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence
from ..interfaces.preference_interface import IPreferencesPersistence
from ..interfaces.building_interface import IBuildingsPersistence

from ...objects.rating import Rating
from ..common import get_current_user_id
from ...exceptions.throne_validation_exception import ThroneValidationException
from typing import Optional, Any


class ReviewStore:
    def __init__(
        self,
        review_persistence: IReviewsPersistence,
        rating_persistence: IRatingsPersistence,
        user_persistence: IUsersPersistence,
        preference_persistence: IPreferencesPersistence,
        washroom_persistence: IWashroomsPersistence,
        building_persistence: IBuildingsPersistence
    ):
        self.__review_persistence: IReviewsPersistence = review_persistence
        self.__rating_persistence: IRatingsPersistence = rating_persistence
        self.__user_persistence: IUsersPersistence = user_persistence
        self.__preference_persistence: IPreferencesPersistence = \
            preference_persistence
        self.__washroom_persistence: IWashroomsPersistence = \
            washroom_persistence
        self.__building_persistence: IBuildingsPersistence = \
            building_persistence

    def create_review(
        self,
        washroom_id: int,
        comment: str,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float
    ) -> Optional[dict]:
        if self.__washroom_persistence.get_washroom(washroom_id) is None:
            raise ThroneValidationException("Washroom id is not valid")

        if not len(comment) > 0:
            raise ThroneValidationException("Comment cannot be an empty string")

        if not Rating.verify(
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        ):
            raise ThroneValidationException("Ratings are invalid")

        # Get the user ID
        user_id = get_current_user_id(
            self.__user_persistence,
            self.__preference_persistence
        )

        # Add the rating
        rating_id = self.__rating_persistence.add_rating(
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        )
        # Add the review
        review_id = self.__review_persistence.add_review(
            washroom_id,
            user_id,
            rating_id,
            comment,
            0
        )

        # Update the washroom rating
        self.__update_washroom_rating(
            washroom_id,
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        )
        # Update the building rating
        self.__update_building_rating(
            washroom_id,
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        )

        # Return the review
        review = self.__review_persistence.get_review(review_id)
        result = review.__dict__.copy()
        self.__expand_review(result)
        return result

    def __update_washroom_rating(
        self,
        washroom_id: int,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float
    ):
        # Get the washroom
        washroom = self.__washroom_persistence.get_washroom(
            washroom_id
        )
        # Get the average ratings
        washroom_avg_ratings_id = washroom["average_rating_id"]
        washroom_avg_rating = self.__rating_persistence.get_rating(
            washroom_avg_ratings_id
        )
        # Get the review count of the washrooms
        review_count_washroom = self.__review_persistence.\
            get_review_count_by_washroom(
                washroom_id
            )
        # Update the average washroom rating
        # If the averages are zero, this is our first washroom review
        # Otherwise update the averages
        # Set the averages to the user rating
        if (washroom_avg_rating.cleanliness == 0
            and washroom_avg_rating.privacy == 0
                and washroom_avg_rating.smell == 0
                and washroom_avg_rating.toilet_paper_quality == 0):
            washroom_avg_rating.cleanliness = cleanliness
            washroom_avg_rating.privacy = privacy
            washroom_avg_rating.smell = smell
            washroom_avg_rating.toilet_paper_quality = toilet_paper_quality
            ratings = [
                washroom_avg_rating.cleanliness,
                washroom_avg_rating.privacy,
                washroom_avg_rating.smell,
                washroom_avg_rating.toilet_paper_quality
            ]
        else:
            ratings = [
                washroom_avg_rating.cleanliness,
                washroom_avg_rating.privacy,
                washroom_avg_rating.smell,
                washroom_avg_rating.toilet_paper_quality
            ]
            # Update the averages
            for x in [cleanliness, privacy, smell, toilet_paper_quality]:
                ratings = [((rating * review_count_washroom) + x) /
                           (review_count_washroom + 1) for rating in ratings]
                washroom_avg_rating.cleanliness = ratings[0]
                washroom_avg_rating.privacy = ratings[1]
                washroom_avg_rating.smell = ratings[2]
                washroom_avg_rating.toilet_paper_quality = ratings[3]

        # Actually update DB with the new rating
        self.__rating_persistence.update_rating(
            washroom_avg_ratings_id,
            washroom_avg_rating.cleanliness,
            washroom_avg_rating.privacy,
            washroom_avg_rating.smell,
            washroom_avg_rating.toilet_paper_quality
        )
        # Update the overall rating for the washroom
        new_overall_rating = sum(ratings) / len(ratings)
        self.__washroom_persistence.update_washroom(
            washroom_id,
            washroom.title,
            washroom.location,
            washroom.floor,
            washroom.gender,
            washroom.amenities_id,
            new_overall_rating,
            washroom_avg_ratings_id
        )

    def __update_building_rating(
        self,
        washroom_id: int
    ):
        # Get the washroom
        washroom = self.__washroom_persistence.get_washroom(
            washroom_id
        )
        # Get the average ratings
        washroom_avg_ratings_id = washroom["average_rating_id"]
        washroom_avg_rating = self.__rating_persistence.get_rating(
            washroom_avg_ratings_id
        )
        # Get the building
        building = self.__building_persistence.get_building(
            washroom.building_id
        )
        # Get the best ratings for this building
        building_best_ratings_id = building["best_ratings_id"]
        building_best_ratings = self.__rating_persistence.get_rating(
            building_best_ratings_id
        )
        washroom_ratings = [
                washroom_avg_rating.cleanliness,
                washroom_avg_rating.privacy,
                washroom_avg_rating.smell,
                washroom_avg_rating.toilet_paper_quality
            ]
        building_ratings = [
            building_best_ratings.cleanliness,
            building_best_ratings.privacy,
            building_best_ratings.smell,
            building_best_ratings.toilet_paper_quality
        ]

        # Update the best building ratings
        for x in washroom_ratings:
            building_ratings = [max(rating, x) for rating in building_ratings]
            building_best_ratings.cleanliness = building_ratings[0]
            building_best_ratings.privacy = building_ratings[1]
            building_best_ratings.smell = building_ratings[2]
            building_best_ratings.toilet_paper_quality = building_ratings[3]
        # Actually update the DB with the new ratings
        self.__rating_persistence.update_rating(
            building_best_ratings_id,
            building_best_ratings.cleanliness,
            building_best_ratings.privacy,
            building_best_ratings.smell,
            building_best_ratings.toilet_paper_quality
        )
        # Update the overall rating for the building
        new_overall_rating = sum(building_ratings) / len(building_ratings)
        self.__building_persistence.update_building(
            building.id,
            building.location,
            building.title,
            building.maps_service_id,
            new_overall_rating,
            building_best_ratings_id
        )

    def update_review(
        self,
        washroom_id: int,
        comment: str,
        ratings: dict
    ) -> Optional[dict]:
        # TODO: Add support for updating a Review based
        # on the provided data - If data is invalid, throw
        # and exception
        return None

    def delete_review(
        self,
        review_id: int
    ) -> None:
        # TODO: Add support for deleting a Review based
        # on the provided data - If data is invalid, throw
        # and exception
        pass

    def get_review(self, review_id: int) -> dict:
        result: Any = self.__review_persistence.get_review(
            review_id
        )
        if result:
            result = result.__dict__.copy()
            self.__expand_review(result)
        return result

    def __expand_review(self, review: dict) -> None:
        # Expand ratings
        rating_id = review.pop("rating_id", None)
        rating_item = self.__rating_persistence.get_rating(
            rating_id
        ).__dict__.copy()

        rating_item.pop("id", None)
        review["ratings"] = rating_item

        user_id = review.pop("user_id", None)
        user_item = self.__user_persistence.get_user(
            user_id
        ).__dict__.copy()
        user_item.pop("preference_id", None)
        user_item.pop("created_at", None)
        review["user"] = user_item
