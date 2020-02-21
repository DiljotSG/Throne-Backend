from abc import ABC
from abc import abstractmethod


class IFavoritesPersistence(ABC):
    @abstractmethod
    def add_favorite(
        self,
        user_id,  # Foreign Key
        washroom_id  # Foreign Key
    ):
        # Return Favorite id
        pass

    @abstractmethod
    def get_favorite(
        self,
        favorite_id
    ):
        pass

    @abstractmethod
    def get_favorites_by_user(
        self,
        user_id  # Foreign Key
    ):
        pass

    @abstractmethod
    def remove_favorite(
        self,
        favorite_id
    ):
        pass
