from ..interfaces.favorite_interface import IFavoritesPersistence
from ...objects.favorite import Favorite

from typing import Optional, List


class FavoritesStubPersistence(IFavoritesPersistence):
    def __init__(self) -> None:
        self.favorites: List[Favorite] = []

    def add_favorite(
        self,
        user_id: int,  # Foreign Key
        washroom_id: int  # Foreign Key
    ) -> int:
        favorite_id = len(self.favorites)
        new_favorite = Favorite(
            favorite_id,
            user_id,
            washroom_id
        )
        self.favorites.append(new_favorite)
        # Return Favorite id
        return favorite_id

    def get_favorite(
        self,
        favorite_id: int
    ) -> Optional[Favorite]:
        if favorite_id >= 0 and favorite_id < len(self.favorites) and \
           self.favorites[favorite_id] is not None:
            return self.favorites[favorite_id]
        return None

    def get_favorites_by_user(
        self,
        user_id: int  # Foreign Key
    ) -> Optional[List[Favorite]]:
        user_favorites = []
        for favorite in self.favorites:
            if favorite is not None and user_id == favorite.user_id:
                user_favorites.append(favorite)

        return user_favorites

    def remove_favorite(
        self,
        favorite_id: int
    ) -> None:
        if favorite_id >= 0 and favorite_id < len(self.favorites):
            self.favorites.pop(favorite_id)
