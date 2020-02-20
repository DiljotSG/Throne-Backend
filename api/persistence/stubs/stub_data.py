from ...objects.location import Location
from ...db_objects.amenity import Amenity


def populate_stub_data(
    amenity_persistence,
    building_persistence,
    favorite_persistence,
    preference_persistence,
    rating_persistence,
    review_persistence,
    user_persistence,
    washroom_persistence
):
    users = create_users(preference_persistence, user_persistence)
    ratings = create_ratings(rating_persistence)
    building_best_ratings = create_building_best_ratings(rating_persistence)
    buildings = create_buildings(building_persistence, building_best_ratings)
    amenities = create_amenities(amenity_persistence)
    washrooms = create_washrooms(
        washroom_persistence,
        buildings,
        amenities,
        ratings
    )
    create_reviews(review_persistence, users, washrooms, ratings)
    create_favorites(favorite_persistence, users, washrooms)


# Favorite parameters:
    # user_id
    # washroom_id
def create_favorites(favorite_persistence, users, washrooms):
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
def create_reviews(review_persistence, users, washrooms, ratings):
    review_persistence.add_review(
        washrooms[0],
        users[0],
        ratings[2],
        "yay",
        5
    )

    review_persistence.add_review(
        washrooms[1],
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
def create_ratings(rating_persistence):
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
def create_building_best_ratings(rating_persistence):
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
def create_washrooms(washroom_persistence, buildings, amenities, ratings):
    location1 = Location(12.2, 17.9).__dict__
    location2 = Location(114, 200.5).__dict__

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


def create_amenities(amenity_persistence):
    amenity1_id = amenity_persistence.add_amenities(
        Amenity.AIR_DRYER,
        Amenity.AUTOMATIC_TOILET
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
def create_buildings(building_persistence, building_best_ratings):
    location1 = Location(10.2, 15.9).__dict__
    location2 = Location(104, 230.5).__dict__

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
def create_users(preference_persistence, user_persistence):
    user_preferences_ids = create_preferences(preference_persistence)

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
def create_preferences(preference_persistence):
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
