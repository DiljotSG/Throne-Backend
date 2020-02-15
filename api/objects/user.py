class User:
    def __init__(self,
                 user_ID,
                 created_at,
                 profile_picture,
                 settings):
        self.user_ID = user_ID
        self.created_at = created_at
        self.profile_picture = profile_picture
        self.settings = settings

        self.washroom_preferences = []
