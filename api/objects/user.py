class User:
    def __init__(
        self,
        user_id,
        username,
        created_at,
        profile_picture,
        preference_id
    ):
        self.id = user_id
        self.username = username
        self.created_at = created_at
        self.profile_picture = profile_picture
        self.preference_id = preference_id
