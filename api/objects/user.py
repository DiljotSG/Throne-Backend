from datetime import datetime
from api.common import get_cognito_user


class User:
    def __init__(
        self,
        user_id: int,
        username: str,
        created_at: datetime,
        profile_picture: str,
        preference_id: int
    ):
        self.id = user_id
        self.username = username
        self.created_at = created_at
        self.profile_picture = profile_picture
        self.preference_id = preference_id

    def to_dict(
        self,
        preference_persistence
    ) -> dict:
        user = self.__dict__.copy()

        # Only expand preferences if the Username matches current user
        if user["username"] == get_cognito_user():
            # Expand preferences
            preference_id = user.pop("preference_id", None)
            user["preferences"] = preference_persistence.get_preference(
                preference_id
            ).to_dict()

        # Cleanup
        user.pop("preference_id", None)
        return user
