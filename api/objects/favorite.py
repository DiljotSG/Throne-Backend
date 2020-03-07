class Favorite:
    def __init__(
        self,
        favorite_id: int,
        user_id: int,
        washroom_id: int
    ) -> None:
        self.id = favorite_id
        self.user_id = user_id
        self.washroom_id = washroom_id

    def to_dict(
        self,
        washroom_persistence,
        building_persistence,
        amenity_persistence,
        ratings_persistence,
        favorite_persistence,
        user_persistence,
        preference_persistence
    ) -> dict:
        favorite = self.__dict__.copy()

        # Remove ids
        favorite.pop("id", None)
        favorite.pop("user_id", None)

        # Expand washroom
        washroom_id = favorite.pop("washroom_id", None)
        item = washroom_persistence.get_washroom(
            washroom_id
        ).to_dict(
            building_persistence,
            amenity_persistence,
            ratings_persistence,
            favorite_persistence,
            user_persistence,
            preference_persistence
        )

        favorite.update(item)

        return favorite
