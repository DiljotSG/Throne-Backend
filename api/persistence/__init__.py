from .stubs.amenity_stub import AmenitiesStubPersistence
from .stubs.building_stub import BuildingsStubPersistence
from .stubs.favorite_stub import FavoritesStubPersistence
from .stubs.preference_stub import PreferencesStubPersistence
from .stubs.rating_stub import RatingsStubPersistence
from .stubs.review_stub import ReviewsStubPersistence
from .stubs.user_stub import UsersStubPersistence
from .stubs.washroom_stub import WashroomsStubPersistence

from .stores.building_store import BuildingStore
from .stores.review_store import ReviewStore
from .stores.user_store import UserStore
from .stores.washroom_store import WashroomStore

import os

if os.environ.get("IS_LAMBDA"):
    # DB implelentation here
    pass
else:
    __amenity_persistence = AmenitiesStubPersistence()
    __building_persistence = BuildingsStubPersistence()
    __favourite_persistence = FavoritesStubPersistence()
    __preference_persistence = PreferencesStubPersistence()
    __rating_persistence = RatingsStubPersistence()
    __review_persistence = ReviewsStubPersistence()
    __user_persistence = UsersStubPersistence()
    __washroom_persistence = WashroomsStubPersistence()


def create_building_store():
    return BuildingStore(
        __building_persistence,
        __washroom_persistence,
        __review_persistence
    )


def create_washroom_store():
    return WashroomStore(
        __washroom_persistence,
        __review_persistence
    )


def create_review_store():
    return ReviewStore(
        __review_persistence
    )


def create_user_store():
    return UserStore(
        __user_persistence,
        __favourite_persistence,
        __review_persistence
    )
