class User:
    def __init__(self,
                 id,
                 timestamp,
                 profile_picture,
                 settings,
                 washroom_preferences):
        self.id = id
        self.timestamp = timestamp
        self.profile_picture = profile_picture
        self.settings = settings
        self.washroom_preferences = washroom_preferences
