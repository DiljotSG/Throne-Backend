from abc import ABC
from abc import abstractmethod


class IRatingsPersistence(ABC):
    @abstractmethod
    def add_rating(
        self,
        cleanliness,
        privacy,
        smell,
        toilet_paper_quality,
    ):
        # Return Rating id
        pass

    @abstractmethod
    def get_rating(
        self,
        rating_id
    ):
        pass

    @abstractmethod
    def remove_rating(
        self,
        rating_id
    ):
        pass
