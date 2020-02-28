class Rating:
    def __init__(
        self,
        rating_id: int,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float
    ):
        self.id = rating_id
        self.cleanliness = cleanliness
        self.privacy = privacy
        self.smell = smell
        self.toilet_paper_quality = toilet_paper_quality
