from abc import ABC
from abc import abstractmethod
from ...objects.user import User


class IUsersPersistence(ABC):

    @abstractmethod
    def add_user(
        self,
        username: str,
        profile_pic: str,
        preference_id: int  # Foreign key
    ) -> int:
        # Return User id
        pass

    @abstractmethod
    def get_user(
        self,
        user_id: int
    ) -> User:
        pass

    @abstractmethod
    def remove_user(
        self,
        user_id: int
    ) -> None:
        pass
