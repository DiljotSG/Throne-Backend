from ..interfaces.amenity_interface import IAmenitiesPersistence
from ..interfaces.building_interface import IBuildingsPersistence
from ..interfaces.favorite_interface import IFavoritesPersistence
from ..interfaces.preference_interface import IPreferencesPersistence
from ..interfaces.rating_interface import IRatingsPersistence
from ..interfaces.review_interface import IReviewsPersistence
from ..interfaces.user_interface import IUsersPersistence
from ..interfaces.washroom_interface import IWashroomsPersistence

from ...objects.amenity import Amenity
from ...objects.location import Location

from typing import List


def populate_stub_data(
    amenity_persistence: IAmenitiesPersistence,
    building_persistence: IBuildingsPersistence,
    favorite_persistence: IFavoritesPersistence,
    preference_persistence: IPreferencesPersistence,
    rating_persistence: IRatingsPersistence,
    review_persistence: IReviewsPersistence,
    user_persistence: IUsersPersistence,
    washroom_persistence: IWashroomsPersistence
) -> None:
    users = __create_users(preference_persistence, user_persistence)
    ratings = __create_ratings(rating_persistence)
    building_best_ratings = __create_building_best_ratings(rating_persistence)
    buildings = __create_buildings(building_persistence, building_best_ratings)
    amenities = __create_amenities(amenity_persistence)
    washrooms = __create_washrooms(
        washroom_persistence,
        buildings,
        amenities,
        ratings
    )
    __create_reviews(
        review_persistence,
        users,
        washrooms,
        ratings,
        ratings
    )
    __create_favorites(favorite_persistence, users, washrooms)


# Favorite parameters:
    # user_id
    # washroom_id
def __create_favorites(
    favorite_persistence: IFavoritesPersistence,
    users: List[int],
    washrooms: List[int]
) -> None:
    favorite_persistence.add_favorite(
        users[0],
        washrooms[0]
    )

    favorite_persistence.add_favorite(
        users[1],
        washrooms[1]
    )


# Review parameters:
    # washroom_id
    # user_id
    # rating_id
    # comment
    # upvote_count
    # ratings
    # ratings for each review
def __create_reviews(
    review_persistence: IReviewsPersistence,
    users: List[int],
    washrooms: List[int],
    ratings: List[int],
    review_ratings: List[int]
) -> None:
    review_persistence.add_review(
        washrooms[0],
        users[0],
        ratings[2],
        "yay",
        5
    )

    review_persistence.add_review(
        washrooms[2],
        users[1],
        ratings[3],
        "boo",
        10
    )


# Ratings parameters:
    # cleanliness
    # privacy
    # smell
    # toilet_paper_quality
def __create_ratings(rating_persistence: IRatingsPersistence) -> List[int]:
    # Average ratings
    rating1 = rating_persistence.add_rating(
        3.2,
        1.2,
        2.7,
        4.5
    )

    rating2 = rating_persistence.add_rating(
        2.2,
        4.2,
        2.8,
        4.2
    )

    # Washroom ratings
    rating3 = rating_persistence.add_rating(
        3.2,
        1.2,
        2.7,
        4.5
    )

    rating4 = rating_persistence.add_rating(
        2.2,
        4.2,
        2.8,
        4.2
    )

    return [rating1, rating2, rating3, rating4]


# Ratings parameters:
    # cleanliness
    # privacy
    # smell
    # toilet_paper_quality
def __create_building_best_ratings(
    rating_persistence: IRatingsPersistence
) -> List[int]:
    # Average ratings
    rating1 = rating_persistence.add_rating(
        3.2,
        1.2,
        2.7,
        4.5
    )

    rating2 = rating_persistence.add_rating(
        2.2,
        4.2,
        2.8,
        4.2
    )

    return [rating1, rating2]


# Washroom Parameters:
    # building_id
    # location
    # title
    # floor
    # gender
    # amenities_id
    # overall_rating
    # average_ratings_id
def __create_washrooms(
    washroom_persistence: IWashroomsPersistence,
    buildings: List[int],
    amenities: List[int],
    ratings: List[int]
) -> List[int]:
    location1 = Location(12.2, 17.9)
    location2 = Location(114, 200.5)

    washroom1_id = washroom_persistence.add_washroom(
        buildings[0],
        location1,
        "Engineering 1",
        1,
        "women",
        amenities[0],
        4,
        ratings[0]
    )

    washroom2_id = washroom_persistence.add_washroom(
        buildings[0],
        location2,
        "Engineering 2",
        1,
        "men",
        amenities[0],
        3,
        ratings[0]
    )

    washroom3_id = washroom_persistence.add_washroom(
        buildings[1],
        location2,
        "Science 1",
        1,
        "men",
        amenities[1],
        3,
        ratings[1]
    )

    return [washroom1_id, washroom2_id, washroom3_id]


def __create_amenities(
    amenity_persistence: IAmenitiesPersistence
) -> List[int]:
    amenity1_id = amenity_persistence.add_amenities(
        Amenity.AIR_DRYER,
        Amenity.AUTO_TOILET
    )
    amenity2_id = amenity_persistence.add_amenities(
        Amenity.CONTRACEPTION,
        Amenity.LOTION
    )

    return [amenity1_id, amenity2_id]


# Building parameters:
    # location
    # title
    # map_service_id
    # overall_rating
    # ratings
    # best ratings for each building
def __create_buildings(
    building_persistence: IBuildingsPersistence,
    building_best_ratings: List[int]
) -> List[int]:
    location1 = Location(10.2, 15.9)
    location2 = Location(104, 230.5)

    building1_id = building_persistence.add_building(
        location1,
        "Engineering",
        0,
        4,
        building_best_ratings[0]
    )

    building2_id = building_persistence.add_building(
        location2,
        "Science",
        1,
        3,
        building_best_ratings[1]
    )

    return [building1_id, building2_id]


# User parameters:
    # username
    # profile_pic
    # preference_id
def __create_users(
    preference_persistence: IPreferencesPersistence,
    user_persistence: IUsersPersistence
) -> List[int]:
    user_preferences_ids = __create_preferences(preference_persistence)

    user1_id = user_persistence.add_user(
        "janesmith",
        "picture",
        user_preferences_ids[0]
    )

    user2_id = user_persistence.add_user(
        "johnsmith",
        "picture",
        user_preferences_ids[1]
    )

    return [user1_id, user2_id]


# Preferences paramaters:
    # gender
    # wheelchair_accessible
    # main_floor_access
def __create_preferences(
    preference_persistence: IPreferencesPersistence
) -> List[int]:
    user_pref1_id = preference_persistence.add_preference(
        "women",
        True,
        False
    )

    user_pref2_id = preference_persistence.add_preference(
        "men",
        False,
        True
    )

    return [user_pref1_id, user_pref2_id]
