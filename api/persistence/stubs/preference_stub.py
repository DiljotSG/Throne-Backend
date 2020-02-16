from interfaces.preference_interface import IPreferencesPersistence


class PreferencesPersistence(IPreferencesPersistence):
    def add_preference(
        self,
        gender,
        wheelchair_accessible,
        main_floor_access
    ):
        # Return Preference id
        pass

    def get_preference(
        self,
        preference_id
    ):
        pass

    def remove_preference(
        self,
        preference_id
    ):
        pass
