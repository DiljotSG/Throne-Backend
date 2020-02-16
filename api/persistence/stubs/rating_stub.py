from interfaces.rating_interface import IRatingsPersistence


class RatingsPersistence(IRatingsPersistence):
    def add_rating(
        self,
        cleanliness,
        privacy,
        smell,
        toilet_paper_ply,
    ):
        # Return Rating id
        pass

    def get_rating(
        self,
        rating_id
    ):
        pass

    def remove_rating(
        self,
        rating_id
    ):
        pass
