from abc import ABC
from abc import abstractmethod


class IPreferencesPersistence(ABC):
    @abstractmethod
    def add_preference(
        self,
        gender,
        wheelchair_accessible,
        main_floor_access
    ):
        # Return Preference id
        pass

    @abstractmethod
    def get_preference(
        self,
        preference_id
    ):
        pass

    @abstractmethod
    def remove_preference(
        self,
        preference_id
    ):
        pass
