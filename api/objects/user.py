from datetime import datetime


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
