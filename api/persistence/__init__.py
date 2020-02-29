from .stubs.amenity_stub import AmenitiesStubPersistence
from .stubs.building_stub import BuildingsStubPersistence
from .stubs.favorite_stub import FavoritesStubPersistence
from .stubs.preference_stub import PreferencesStubPersistence
from .stubs.rating_stub import RatingsStubPersistence
from .stubs.review_stub import ReviewsStubPersistence
from .stubs.user_stub import UsersStubPersistence
from .stubs.washroom_stub import WashroomsStubPersistence

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
from api.common import should_use_db
from api.common import get_cognito_user


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
        __user_persistence
    )


def create_review_store() -> ReviewStore:
    return ReviewStore(
        __review_persistence,
        __rating_persistence,
        __user_persistence
    )


def create_user_store() -> UserStore:
    return UserStore(
        __user_persistence,
        __favorite_persistence,
        __review_persistence,
        __preference_persistence,
        __rating_persistence
    )


# Gives the currently authenticated user's ID
def get_current_user_id(self) -> int:
    # Default user ID for the Stubs is 0
    user_id: int = 0

    # If we are using the DB, we can fetch user ID
    if should_use_db():
        # Try to get the current user's username
        username = get_cognito_user()
        # We can only get the username if this is the Lambda
        # If we get None back, we are not running in the Lambda
        if username:
            # Is this user in the Users table?
            # Try to fetch the user from the table
            opt_user_id = self.__user_persistence.get_id_by_username(
                username
            )

            # Check that the user ID is not None before we assign it
            # This makes the static type checker happy
            if opt_user_id is not None:
                user_id = opt_user_id

            # If they don't have a user ID, we haven't
            # inserted them into the Users table yet.
            # Let's do that now
            if opt_user_id is None:
                # Make their preferences object first
                pref_id = self.__preference_persistence.add_preference(
                    "undefined",
                    False,
                    False
                )

                # Finally insert this user into the Users table
                user_id = self.__user_persistence.add_user(
                    username,
                    "default",
                    pref_id
                )

    # We did it! We got the user ID finally.
    return user_id
