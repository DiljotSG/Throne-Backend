from typing import Optional, List

from ..interfaces.preference_interface import IPreferencesPersistence
from ...objects.preference import Preference


class PreferencesStubPersistence(IPreferencesPersistence):
    def __init__(self) -> None:
        self.preferences: List[Preference] = []

    def add_preference(
        self,
        gender: str,
        wheelchair_accessible: bool,
        main_floor_access: bool
    ) -> int:
        preference_id = len(self.preferences)
        new_preference = Preference(
            preference_id,
            gender,
            wheelchair_accessible,
            main_floor_access
        )
        # Return Preference id
        self.preferences.append(new_preference)
        return preference_id

    def update_preference(
        self,
        preference_id: int,
        gender: str,
        wheelchair_accessible: bool,
        main_floor_access: bool
    ) -> Optional[Preference]:
        updated_pref = None
        if preference_id >= 0 and preference_id < len(self.preferences) and \
           self.preferences[preference_id] is not None:
            updated_pref = Preference(
                preference_id,
                gender,
                wheelchair_accessible,
                main_floor_access
            )
            self.preferences[preference_id] = updated_pref
        return updated_pref

    def get_preference(
        self,
        preference_id: int
    ) -> Optional[Preference]:
        if preference_id >= 0 and preference_id < len(self.preferences) and \
           self.preferences[preference_id] is not None:
            return self.preferences[preference_id]
        return None

    def remove_preference(
        self,
        preference_id: int
    ) -> None:
        if preference_id >= 0 and preference_id < len(self.preferences):
            self.preferences.pop(preference_id)
