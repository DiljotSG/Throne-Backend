from interfaces.favorite_interface import IFavoritesPersistence


class FavoritesPersistence(IFavoritesPersistence):
    def add_favorite(
        self,
        user_id,  # Foreign Key
        washroom_id  # Foreign Key
    ):
        # Return Favorite id
        pass

    def get_favorite(
        self,
        favorite_id
    ):
        pass

    def get_favorites_for_user(
        self,
        user_id  # Foreign Key
    ):
        pass

    def remove_favorite(
        self,
        favorite_id
    ):
        pass
