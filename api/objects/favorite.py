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
