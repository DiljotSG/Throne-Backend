class User:
    def __init__(self,
                 id,
                 created_at,
                 profile_picture,
                 settings):
        self.id = id
        self.created_at = created_at
        self.profile_picture = profile_picture
        self.settings = settings

        self.washroom_preferences = []
