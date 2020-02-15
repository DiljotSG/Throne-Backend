class Review:
    def __init__(self,
                 review_ID,
                 washroom_ID,
                 created_at,
                 comment,
                 upvote_count):
        self.review_ID = review_ID
        self.washroom_ID = washroom_ID
        self.created_at = created_at
        self.comment = comment
        self.upvote_count = upvote_count

        self.ratings = []
