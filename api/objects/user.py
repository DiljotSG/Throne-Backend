class User:
    def __init__(self,
                 id,
                 timestamp,
                 profile_picture,
                 settings):
        self.id = id
        self.timestamp = timestamp
        self.profile_picture = profile_picture
        self.settings = settings

        washroom_preferences = []
