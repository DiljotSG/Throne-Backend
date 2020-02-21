class Review:
    def __init__(
        self,
        review_id,
        washroom_id,
        user_id,
        created_at,
        comment,
        upvote_count,
        rating_id
    ):
        self.id = review_id
        self.washroom_id = washroom_id
        self.user_id = user_id
        self.created_at = created_at
        self.comment = comment
        self.upvote_count = upvote_count
        self.rating_id = rating_id
