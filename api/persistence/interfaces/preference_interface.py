from abc import ABC
from abc import abstractmethod
from ...objects.preference import Preference


class IPreferencesPersistence(ABC):
    @abstractmethod
    def add_preference(
        self,
        gender: str,
        wheelchair_accessible: bool,
        main_floor_access: bool
    ) -> int:
        # Return Preference id
        pass

    @abstractmethod
    def update_preference(
        self,
        preference_id: int,
        gender: str,
        wheelchair_accessible: bool,
        main_floor_access: bool
    ) -> Preference:
        pass

    @abstractmethod
    def get_preference(
        self,
        preference_id: int
    ) -> Preference:
        pass

    @abstractmethod
    def remove_preference(
        self,
        preference_id: int
    ) -> None:
        pass
