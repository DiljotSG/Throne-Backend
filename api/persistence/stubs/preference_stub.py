from interfaces.preference_interface import IPreferencesPersistence
from ... stub_objects.preference import Preference


class PreferencesStubPersistence(IPreferencesPersistence):
    def __init__(self):
        self.preferences = []

    def add_preference(
        self,
        gender,
        wheelchair_accessible,
        main_floor_access
    ):
        preference_id = len(self.preferences)
        new_preference = Preference(preference_id,
                                    gender,
                                    wheelchair_accessible,
                                    main_floor_access)
        # Return Preference id
        self.preferences.append(new_preference)
        return preference_id

    def get_preference(
        self,
        preference_id
    ):
        return self.preferences[preference_id]

    def remove_preference(
        self,
        preference_id
    ):
        self.preferences.pop(preference_id)
