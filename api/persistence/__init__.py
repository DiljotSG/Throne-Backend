from .stubs.amenity_stub import AmenitiesStubPersistence
from .stubs.building_stub import BuildingsStubPersistence
from .stubs.favorite_stub import FavoritesStubPersistence
from .stubs.preference_stub import PreferencesStubPersistence
from .stubs.rating_stub import RatingsStubPersistence
from .stubs.review_stub import ReviewsStubPersistence
from .stubs.user_stub import UsersStubPersistence
from .stubs.washroom_stub import WashroomsStubPersistence

from .stores.building_store import BuildingStore

# If Debug
amenity_persistence = AmenitiesStubPersistence()
building_persistence = BuildingsStubPersistence()
favourite_persistence = FavoritesStubPersistence()
preference_persistence = PreferencesStubPersistence()
rating_persistence = RatingsStubPersistence()
review_persistence = ReviewsStubPersistence()
user_persistence = UsersStubPersistence()
washroom_persistence = WashroomsStubPersistence()
# else
# amenity_persistence = AmenitiesDBPersistence()
# ....


def create_building_store():
    return BuildingStore(
        building_persistence,
        washroom_persistence,
        review_persistence
    )


def create_washroom_store():
    # return WashroomStore(washroom_persistence, building_persistence, ...)
    pass


def create_review_store():
    # return ReviewStore(reivew_persistence, building_persistence, ..., )
    pass


def create_user_store():
    # return UserStore(user_persistence, ...)
    pass
