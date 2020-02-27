class Preference:
    def __init__(
        self,
        preference_id,
        gender,
        wheelchair_accessible,
        main_floor_access
    ):
        self.id = preference_id
        self.gender = gender
        self.wheelchair_accessible = wheelchair_accessible
        self.main_floor_access = main_floor_access
