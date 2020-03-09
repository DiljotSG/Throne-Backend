from api.common import should_use_db
from .implementations.amenity_impl import AmenitiesPersistence
from .implementations.building_impl import BuildingsPersistence
from .implementations.favorite_impl import FavoritesPersistence
from .implementations.preference_impl import PreferencesPersistence
from .implementations.rating_impl import RatingsPersistence
from .implementations.review_impl import ReviewsPersistence
from .implementations.user_impl import UsersPersistence
from .implementations.washroom_impl import WashroomsPersistence
from .interfaces.amenity_interface import IAmenitiesPersistence
from .interfaces.building_interface import IBuildingsPersistence
from .interfaces.favorite_interface import IFavoritesPersistence
from .interfaces.preference_interface import IPreferencesPersistence
from .interfaces.rating_interface import IRatingsPersistence
from .interfaces.review_interface import IReviewsPersistence
from .interfaces.user_interface import IUsersPersistence
from .interfaces.washroom_interface import IWashroomsPersistence
from .stores.building_store import BuildingStore
from .stores.review_store import ReviewStore
from .stores.user_store import UserStore
from .stores.washroom_store import WashroomStore
from .stubs import populate_stub_data
from .stubs.amenity_stub import AmenitiesStubPersistence
from .stubs.building_stub import BuildingsStubPersistence
from .stubs.favorite_stub import FavoritesStubPersistence
from .stubs.preference_stub import PreferencesStubPersistence
from .stubs.rating_stub import RatingsStubPersistence
from .stubs.review_stub import ReviewsStubPersistence
from .stubs.user_stub import UsersStubPersistence
from .stubs.washroom_stub import WashroomsStubPersistence

# Make the Stubs
__amenity_persistence: IAmenitiesPersistence = AmenitiesStubPersistence()
__building_persistence: IBuildingsPersistence = BuildingsStubPersistence()
__favorite_persistence: IFavoritesPersistence = FavoritesStubPersistence()
__preference_persistence: IPreferencesPersistence = \
    PreferencesStubPersistence()
__rating_persistence: IRatingsPersistence = RatingsStubPersistence()
__review_persistence: IReviewsPersistence = ReviewsStubPersistence()
__user_persistence: IUsersPersistence = UsersStubPersistence()
__washroom_persistence: IWashroomsPersistence = WashroomsStubPersistence()


if should_use_db():
    # Use the DB and replace the Stubs
    __amenity_persistence = AmenitiesPersistence()
    __building_persistence = BuildingsPersistence()
    __favorite_persistence = FavoritesPersistence()
    __preference_persistence = PreferencesPersistence()
    __rating_persistence = RatingsPersistence()
    __review_persistence = ReviewsPersistence()
    __user_persistence = UsersPersistence()
    __washroom_persistence = WashroomsPersistence()
else:
    # Init the Stubs
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


def create_building_store() -> BuildingStore:
    return BuildingStore(
        __building_persistence,
        __washroom_persistence,
        __review_persistence,
        __rating_persistence
    )


def create_washroom_store() -> WashroomStore:
    return WashroomStore(
        __washroom_persistence,
        __review_persistence,
        __amenity_persistence,
        __rating_persistence,
        __user_persistence,
        __building_persistence,
        __favorite_persistence,
        __preference_persistence
    )


def create_review_store() -> ReviewStore:
    return ReviewStore(
        __review_persistence,
        __rating_persistence,
        __user_persistence,
        __preference_persistence,
        __washroom_persistence,
        __building_persistence
    )


def create_user_store() -> UserStore:
    return UserStore(
        __user_persistence,
        __favorite_persistence,
        __review_persistence,
        __preference_persistence,
        __rating_persistence,
        __washroom_persistence,
        __building_persistence,
        __amenity_persistence
    )
