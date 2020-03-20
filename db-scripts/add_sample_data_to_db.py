from api.persistence.implementations.amenity_impl import AmenitiesPersistence
from api.persistence.implementations.building_impl import BuildingsPersistence
from api.persistence.implementations.favorite_impl import FavoritesPersistence
from api.persistence.\
    implementations.preference_impl import PreferencesPersistence
from api.persistence.implementations.rating_impl import RatingsPersistence
from api.persistence.implementations.review_impl import ReviewsPersistence
from api.persistence.implementations.user_impl import UsersPersistence
from api.persistence.implementations.washroom_impl import WashroomsPersistence

from api.objects.amenity import Amenity
from api.objects.location import Location

a = AmenitiesPersistence()
b = BuildingsPersistence()
f = FavoritesPersistence()
p = PreferencesPersistence()
ra = RatingsPersistence()
re = ReviewsPersistence()
u = UsersPersistence()
w = WashroomsPersistence()

bRating_good_id = ra.add_rating(4, 5, 1, 4)
bRating_bad_id = ra.add_rating(2, 1, 5, 2)
wRating_good_id = ra.add_rating(5, 5, 1, 5)
wRating_bad_id = ra.add_rating(1, 1, 5, 1)
rRating_good_id = ra.add_rating(5, 4, 2, 5)
rRating_bad_id = ra.add_rating(1, 2, 4, 1)

wAmenities_good_id = a.add_amenities(
    [
        Amenity.AIR_DRYER,
        Amenity.AUTO_SINK,
        Amenity.AUTO_TOILET
    ]
)
wAmenities_bad_id = a.add_amenities(
    [
        Amenity.LOTION,
        Amenity.CONTRACEPTION
    ]
)
uPreferences_good_id = p.add_preference(
    'women',
    False,
    False
)
uPreferences_bad_id = p.add_preference(
    'men',
    False,
    False
)

# Create the building
good_building = b.add_building(
    Location(49.8105, -97.1335),
    'GoodBuilding',
    '',
    5,
    bRating_good_id
)
bad_building = b.add_building(
    Location(49.8096, -97.1328),
    'BadBuilding',
    '',
    1,
    bRating_bad_id
)

# Create the washroom
washroom_good_id = w.add_washroom(
    good_building,
    Location(49.8105, -97.1335),
    'Excellent Washroom 1',
    1,
    'women',
    wAmenities_good_id,
    5,
    wRating_good_id
)
washroom_bad_id = w.add_washroom(
    bad_building,
    Location(49.8096, -97.1328),
    'Terrible Washroom 1',
    8,
    'men',
    wAmenities_bad_id,
    5,
    wRating_bad_id
)

# Create the user
user_good_id = u.add_user(
    'totallyRealWomenUser1',
    'defaultPic1',
    uPreferences_good_id
)
user_bad_id = u.add_user(
    'totallyRealManUser1',
    'defaultPic2',
    uPreferences_bad_id
)

fav_id = f.add_favorite(user_good_id, washroom_good_id)
fav_id = f.add_favorite(user_bad_id, washroom_bad_id)

review_good_id = re.add_review(
    washroom_good_id,
    user_good_id,
    rRating_good_id,
    'So amazing! Smelled like flowers.',
    120
)
review_bad_id = re.add_review(
    washroom_bad_id,
    user_bad_id,
    rRating_bad_id,
    'SMELLS BAD!',
    542
)

print("Done!")
