from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.user_interface import IUsersPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence
from ..interfaces.preference_interface import IPreferencesPersistence
from ..interfaces.building_interface import IBuildingsPersistence

from ...objects.rating import Rating
from ...objects.washroom import Washroom
from ...objects.building import Building
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
        washroom = self.__washroom_persistence.get_washroom(washroom_id)

        if washroom is None:
            raise ThroneValidationException("Washroom id is not valid")

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
        self.__update_washroom_average_and_overall(
            washroom,
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality,
            True
        )

        # Update the building
        self.__update_building_rating(
            washroom
        )

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

        # retrieve and extract dict from review object
        review = self.__review_persistence.get_review(review_id)
        result = review.__dict__.copy()
        self.__expand_review(result)

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
            raise ThroneValidationException("Washroom id is not valid")

        if review is None:
            raise ThroneValidationException("Review id is not valid")

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
        self.__update_washroom_average_and_overall(
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

        # Get the building
        building = self.__building_persistence.get_building(
            washroom.building_id
        )

        if building is None:
            return None

        # Get the next best washroom and it's rating
        next_best_washroom = self.__get_next_best_washroom(
            washroom.building_id
        )

        if next_best_washroom is None:
            return None

        next_best_washroom_rating = self.__rating_persistence.get_rating(
            next_best_washroom.average_rating_id
        )

        if next_best_washroom_rating is None:
            return None

        # Update the building by rolling back to the washroom
        # with the next best rating
        self.__set_building_rating_and_overall(
            building,
            next_best_washroom_rating
        )

        # Return the updated review
        result = review.__dict__.copy()
        self.__expand_review(result)

        return result

    def get_review(self, review_id: int) -> dict:
        result: Any = self.__review_persistence.get_review(
            review_id
        )
        if result:
            result = result.__dict__.copy()
            self.__expand_review(result)
        return result

    def __update_washroom_average_and_overall(
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
            return

        # Get the number of reviews found
        review_cnt = self.__review_persistence.\
            get_review_count_by_washroom(
                washroom.id
            )

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

        # Update the overall average
        self.__washroom_persistence.update_washroom(
            washroom.id,
            washroom.title,
            washroom.location,
            washroom.floor,
            washroom.gender,
            washroom.amenities_id,
            new_overall_average,
            washroom.average_rating_id
        )

    def __get_next_best_washroom(
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

    def __set_building_rating_and_overall(
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

        self.__building_persistence.update_building(
            building.id,
            building.location,
            building.title,
            building.maps_service_id,
            new_overall,
            building.best_ratings_id
        )

    def __update_building_rating(
        self,
        washroom: Washroom
    ) -> None:
        # Get the average washroom rating
        washroom_average_rating = self.__rating_persistence.get_rating(
            washroom.average_rating_id
        )

        if washroom_average_rating is None:
            return

        # Get the building the washroom is in
        building = self.__building_persistence.get_building(
            washroom.building_id
        )

        if building is None:
            return

        # Get the building's best washroom
        building_best_rating = self.__rating_persistence.get_rating(
            building.best_ratings_id
        )

        if building_best_rating is None:
            return

        # Collect values
        washroom_rating_values = [
            washroom_average_rating.cleanliness,
            washroom_average_rating.privacy,
            washroom_average_rating.smell,
            washroom_average_rating.toilet_paper_quality
        ]

        building_rating_values = [
            building_best_rating.cleanliness,
            building_best_rating.privacy,
            building_best_rating.smell,
            building_best_rating.toilet_paper_quality
        ]

        # Only update the building's best and the building's overall
        # if its better than what we've seen previously
        if sum(building_rating_values) < sum(washroom_rating_values):
            self.__set_building_rating_and_overall(
                building,
                washroom_average_rating
            )

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
