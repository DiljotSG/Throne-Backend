class Review:
    def __init__(
        self,
        review_id,
        washroom_id,
        created_at,
        comment,
        upvote_count,
        ratings_id
    ):
        self.id = review_id
        self.washroom_id = washroom_id
        self.created_at = created_at
        self.comment = comment
        self.upvote_count = upvote_count
        self.ratings_id = ratings_id
