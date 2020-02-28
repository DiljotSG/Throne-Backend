

class Review:
    def __init__(
        self,
        review_id: int,
        washroom_id: int,
        created_at: str,
        user_id: int,
        comment: str,
        upvote_count: int,
        rating_id: int
    ):
        self.id = review_id
        self.washroom_id = washroom_id
        self.created_at = created_at
        self.user_id = user_id
        self.comment = comment
        self.upvote_count = upvote_count
        self.rating_id = rating_id

    @staticmethod
    def verify(comment: str) -> bool:
        # TODO: Add support for verifying if a comment contains
        # valid input. Ex. is not empty, etc
        return True
