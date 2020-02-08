class Review:
    def __init__(self,
                 id,
                 washroom_ID,
                 timestamp,
                 comment,
                 upvote_count):
        self.id = id
        self.washroom_ID = washroom_ID
        self.timestamp = timestamp
        self.comment = comment
        self.upvote_count = upvote_count

        self.ratings = []
