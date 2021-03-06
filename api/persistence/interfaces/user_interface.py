from abc import ABC
from abc import abstractmethod
from typing import Optional

from ...objects.user import User


class IUsersPersistence(ABC):

    @abstractmethod
    def add_user(
        self,
        username: str,
        profile_pic: str,
        preference_id: int  # Foreign key
    ) -> int:
        pass

    @abstractmethod
    def get_user(
        self,
        user_id: int
    ) -> Optional[User]:
        pass

    @abstractmethod
    def get_id_by_username(
        self,
        username: str
    ) -> Optional[int]:
        pass

    @abstractmethod
    def remove_user(
        self,
        user_id: int
    ) -> None:
        pass
