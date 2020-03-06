from typing import Optional, Any

from ..common import get_current_user_id
from ..interfaces.building_interface import IBuildingsPersistence
from ..interfaces.preference_interface import IPreferencesPersistence
from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.user_interface import IUsersPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence
from ...exceptions.throne_unauthorized_exception import \
    ThroneUnauthorizedException
from ...exceptions.throne_validation_exception import ThroneValidationException
from ...objects.building import Building
from ...objects.rating import Rating
from ...objects.washroom import Washroom


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
        washroom = self.__washroom_persistence.get_washroom(washroom_id)
        user_id = get_current_user_id(
            self.__user_persistence,
            self.__preference_persistence
        )

        if washroom is None:
            raise ThroneValidationException("Washroom id is not valid")

        building = self.__building_persistence.get_building(
            washroom.building_id
        )

        if building is None:
            raise ThroneValidationException("Invalid building")

        if not len(comment) > 0:
            raise ThroneValidationException(
                "Comment cannot be an empty string"
            )

        if not Rating.verify(
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        ):
            raise ThroneValidationException("Ratings are invalid")

        # Update the average and overall ratings
        self.__update_washroom(
            washroom,
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality,
            True
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

        # Get the best washroom and it's rating
        best_washroom = self.__get_best_washroom(
            washroom.building_id
        )
        if best_washroom is None:
            return None  # Done to please mypy

        best_washroom_rating = self.__rating_persistence.get_rating(
            best_washroom.average_rating_id
        )
        if best_washroom_rating is None:
            return None  # Done to please mypy

        # Update the building by rolling back to the washroom
        # with the next best rating
        self.__update_building(
            building,
            best_washroom_rating
        )

        # Retrieve and extract dict from review object
        review = self.__review_persistence.get_review(review_id)

        # Done to make mypy happy
        if review:
            result = review.to_dict(
                self.__rating_persistence,
                self.__user_persistence,
                self.__preference_persistence
            )

        return result

    def update_review(
        self,
        washroom_id: int,
        review_id: int,
        comment: str,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float
    ) -> Optional[dict]:
        washroom = self.__washroom_persistence.get_washroom(washroom_id)
        review = self.__review_persistence.get_review(review_id)

        if washroom is None:
            raise ThroneValidationException("Washroom id is invalid")

        building = self.__building_persistence.get_building(
            washroom.building_id
        )

        if review is None:
            raise ThroneValidationException("Review id is invalid")

        if building is None:
            raise ThroneValidationException("Building is invalid")

        if not len(comment) > 0:
            raise ThroneValidationException(
                "Comment cannot be an empty string"
            )

        if review.user_id != get_current_user_id(
            self.__user_persistence,
            self.__preference_persistence
        ):
            raise ThroneUnauthorizedException()

        if not Rating.verify(
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        ):
            raise ThroneValidationException("Ratings are invalid")

        # Update the average and overall ratings
        self.__update_washroom(
            washroom,
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality,
            False
        )

        # Update the rating
        self.__rating_persistence.update_rating(
            review.rating_id,
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        )

        # Update the review
        review = self.__review_persistence.update_review(
            review_id,
            review.washroom_id,
            review.user_id,
            review.rating_id,
            comment,
            review.upvote_count
        )

        # Get the best washroom and it's rating
        best_washroom = self.__get_best_washroom(
            washroom.building_id
        )
        if best_washroom is None:
            return None  # This is done to make mypy happy

        best_washroom_rating = self.__rating_persistence.get_rating(
            best_washroom.average_rating_id
        )
        if best_washroom_rating is None:
            return None  # This is done to make mypy happy

        # Update the building by rolling back to the washroom
        # with the next best rating
        self.__update_building(
            building,
            best_washroom_rating
        )

        # Done to make mypy happy
        if review:
            # Return the updated review
            result = review.to_dict(
                self.__rating_persistence,
                self.__user_persistence,
                self.__preference_persistence
            )

        return result

    def get_review(self, review_id: int) -> dict:
        result: Any = self.__review_persistence.get_review(
            review_id
        )
        if result:
            result = result.to_dict(
                self.__rating_persistence,
                self.__user_persistence,
                self.__preference_persistence
            )
        return result

    def __update_washroom(
        self,
        washroom: Washroom,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float,
        adding_values: bool
    ) -> None:
        # Get the average rating
        average_rating = self.__rating_persistence.get_rating(
            washroom.average_rating_id
        )

        if average_rating is None:
            return  # This is done to make mypy happy

        # Get the number of reviews found
        review_cnt = washroom.review_count

        # Compute the new average ratings
        avgs = [
            average_rating.cleanliness,
            average_rating.privacy,
            average_rating.smell,
            average_rating.toilet_paper_quality
        ]

        values = [
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        ]

        # Calculate the new average's with us adding the
        # new ratings to the average
        if adding_values:
            for i, v in enumerate(values):
                avgs[i] = ((avgs[i] * review_cnt) + v) / (review_cnt + 1)

        # Calculate the new averages's with us replacing the values
        else:
            for i, v in enumerate(values):
                avgs[i] = (((avgs[i] * review_cnt) - avgs[i]) + v) / review_cnt

        # Update the average rating object
        self.__rating_persistence.update_rating(
            average_rating.id,
            avgs[0],
            avgs[1],
            avgs[2],
            avgs[3]
        )

        # Compute the overall average rating
        new_overall_average = sum(avgs) / len(avgs)

        # Compute new number of reviews
        if adding_values:
            num_reviews = washroom.review_count + 1
        else:
            num_reviews = washroom.review_count

        # Update the overall average
        self.__washroom_persistence.update_washroom(
            washroom.id,
            washroom.comment,
            washroom.location,
            washroom.floor,
            washroom.gender,
            washroom.urinal_count,
            washroom.stall_count,
            washroom.amenities_id,
            new_overall_average,
            washroom.average_rating_id,
            num_reviews
        )

    def __get_best_washroom(
        self,
        building_id: int
    ) -> Optional[Washroom]:
        washrooms = self.__washroom_persistence.get_washrooms_by_building(
            building_id
        )
        best = None
        for w in washrooms:
            if best is None or w.overall_rating > best.overall_rating:
                best = w
        return best

    def __update_building(
        self,
        building: Building,
        rating: Rating
    ) -> None:
        rating_values = [
            rating.cleanliness,
            rating.privacy,
            rating.smell,
            rating.toilet_paper_quality
        ]

        new_overall = sum(rating_values) / len(rating_values)

        self.__rating_persistence.update_rating(
            building.best_ratings_id,
            rating.cleanliness,
            rating.privacy,
            rating.smell,
            rating.toilet_paper_quality
        )

        self.__building_persistence.update_building(
            building.id,
            building.location,
            building.title,
            building.maps_service_id,
            new_overall,
            building.best_ratings_id,
            building.washroom_count
        )
