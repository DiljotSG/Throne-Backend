class Preference:
    def __init__(
        self,
        preference_id: int,
        gender: str,
        wheelchair_accessible: bool,
        main_floor_access: bool
    ) -> None:
        self.id = preference_id
        self.gender = gender
        self.wheelchair_accessible = wheelchair_accessible
        self.main_floor_access = main_floor_access

    def to_dict(self) -> dict:
        preference = self.__dict__.copy()
        preference.pop("id")
        return preference
