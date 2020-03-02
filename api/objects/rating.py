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

    @staticmethod
    def verify(
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float
    ) -> bool:
        return cleanliness > 0 and cleanliness <= 5 and \
            privacy > 0 and privacy <= 5 and \
            smell > 0 and smell <= 5 and \
            toilet_paper_quality > 0 and toilet_paper_quality <= 5
