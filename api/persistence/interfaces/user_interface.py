from abc import ABC
from abc import abstractmethod


class IUsersPersistence(ABC):

    @abstractmethod
    def add_user(
        self,
        username,
        profile_pic,
        preference_id  # Foreign key
    ):
        # Return User id
        pass

    @abstractmethod
    def get_user(
        self,
        user_id
    ):
        pass

    @abstractmethod
    def remove_user(
        self,
        user_id
    ):
        pass
