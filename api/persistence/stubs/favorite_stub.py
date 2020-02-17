from interfaces.favorite_interface import IFavoritesPersistence
from ... stub_objects.favorite import Favorite


class FavoritesPersistence(IFavoritesPersistence):
    def __init__(self):
        self.favorites = []

    def add_favorite(
        self,
        user_id,  # Foreign Key
        washroom_id  # Foreign Key
    ):
        favorite_id = len(self.favorites)
        new_favorite = Favorite(favorite_id, user_id, washroom_id)
        self.favorites.append(new_favorite)
        # Return Favorite id
        return favorite_id

    def get_favorite(
        self,
        favorite_id
    ):
        return self.favorites[favorite_id]

    def get_favorites_for_user(
        self,
        user_id  # Foreign Key
    ):
        user_favorites = []
        for favorite in self.favorites:
            if user_id == favorite.user_id:
                user_favorites.append(favorite)

        return user_favorites

    def remove_favorite(
        self,
        favorite_id
    ):
        self.favorites.pop(favorite_id)
