from abc import ABC
from abc import abstractmethod
from typing import Optional

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
    ) -> Optional[Preference]:
        pass

    @abstractmethod
    def get_preference(
        self,
        preference_id: int
    ) -> Optional[Preference]:
        pass

    @abstractmethod
    def remove_preference(
        self,
        preference_id: int
    ) -> None:
        pass
