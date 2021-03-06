from abc import ABC
from abc import abstractmethod
from typing import Optional, List

from ...objects.favorite import Favorite


class IFavoritesPersistence(ABC):
    @abstractmethod
    def add_favorite(
        self,
        user_id: int,  # Foreign Key
        washroom_id: int  # Foreign Key
    ) -> int:
        # Return Favorite id
        pass

    @abstractmethod
    def get_favorite(
        self,
        favorite_id: int
    ) -> Optional[Favorite]:
        pass

    @abstractmethod
    def get_favorites_by_user(
        self,
        user_id: int  # Foreign Key
    ) -> List[Favorite]:
        pass

    @abstractmethod
    def remove_favorite(
        self,
        favorite_id: int
    ) -> None:
        pass
