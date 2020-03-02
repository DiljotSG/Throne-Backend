from api.common import should_use_db
from api.common import get_cognito_user

from mysql.connector.errors import InterfaceError
from .interfaces.user_interface import IUsersPersistence
from .interfaces.preference_interface import IPreferencesPersistence


# Gives the currently authenticated user's ID
def get_current_user_id(
    user_persistence: IUsersPersistence,
    preference_persistence: IPreferencesPersistence
) -> int:
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
            opt_user_id = user_persistence.get_id_by_username(
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
                pref_id = preference_persistence.add_preference(
                    "undefined",
                    False,
                    False
                )

                try:
                    # Finally insert this user into the Users table
                    user_id = user_persistence.add_user(
                        username,
                        "default",
                        pref_id
                    )
                except InterfaceError:
                    # We already have this user in the table!
                    # Cleanup
                    preference_persistence.remove_preference(pref_id)

                    # Return user ID
                    # Try to fetch the user from the table now
                    opt_user_id = user_persistence.get_id_by_username(
                        username
                    )
                    # Check that the user ID is not None before we assign it
                    # This makes the static type checker happy
                    if opt_user_id is not None:
                        user_id = opt_user_id

    # We did it! We got the user ID finally.
    return user_id
