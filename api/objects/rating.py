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
        return 0 < cleanliness <= 5 and \
               0 < privacy <= 5 and \
               0 < smell <= 5 and \
               0 < toilet_paper_quality <= 5

    def to_dict(self) -> dict:
        rating = self.__dict__.copy()
        rating.pop("id")
        return rating
