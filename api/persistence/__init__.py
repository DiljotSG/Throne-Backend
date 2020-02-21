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
from .stubs.stub_data import populate_stub_data

import os

if os.environ.get("IS_LAMBDA") or os.environ.get("THRONE_USE_DB"):
    # TODO: Change these to DB implementations
    __amenity_persistence = AmenitiesStubPersistence()
    __building_persistence = BuildingsStubPersistence()
    __favorite_persistence = FavoritesStubPersistence()
    __preference_persistence = PreferencesStubPersistence()
    __rating_persistence = RatingsStubPersistence()
    __review_persistence = ReviewsStubPersistence()
    __user_persistence = UsersStubPersistence()
    __washroom_persistence = WashroomsStubPersistence()

    populate_stub_data(
        __amenity_persistence,
        __building_persistence,
        __favorite_persistence,
        __preference_persistence,
        __rating_persistence,
        __review_persistence,
        __user_persistence,
        __washroom_persistence
    )
else:
    __amenity_persistence = AmenitiesStubPersistence()
    __building_persistence = BuildingsStubPersistence()
    __favorite_persistence = FavoritesStubPersistence()
    __preference_persistence = PreferencesStubPersistence()
    __rating_persistence = RatingsStubPersistence()
    __review_persistence = ReviewsStubPersistence()
    __user_persistence = UsersStubPersistence()
    __washroom_persistence = WashroomsStubPersistence()

    populate_stub_data(
        __amenity_persistence,
        __building_persistence,
        __favorite_persistence,
        __preference_persistence,
        __rating_persistence,
        __review_persistence,
        __user_persistence,
        __washroom_persistence
    )


def create_building_store():
    return BuildingStore(
        __building_persistence,
        __washroom_persistence,
        __review_persistence,
        __rating_persistence
    )


def create_washroom_store():
    return WashroomStore(
        __washroom_persistence,
        __review_persistence,
        __amenity_persistence,
        __rating_persistence
    )


def create_review_store():
    return ReviewStore(
        __review_persistence,
        __rating_persistence
    )


def create_user_store():
    return UserStore(
        __user_persistence,
        __favorite_persistence,
        __review_persistence,
        __preference_persistence,
        __rating_persistence
    )
