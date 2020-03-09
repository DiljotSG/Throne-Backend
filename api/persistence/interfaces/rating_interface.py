from abc import ABC
from abc import abstractmethod
from typing import Optional

from ...objects.rating import Rating


class IRatingsPersistence(ABC):
    @abstractmethod
    def add_rating(
        self,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float,
    ) -> int:
        # Return Rating id
        pass

    @abstractmethod
    def get_rating(
        self,
        rating_id: int
    ) -> Optional[Rating]:
        pass

    @abstractmethod
    def update_rating(
        self,
        rating_id: int,
        cleanliness: float,
        privacy: float,
        smell: float,
        toilet_paper_quality: float
    ) -> Optional[Rating]:
        pass

    @abstractmethod
    def remove_rating(
        self,
        rating_id: int
    ) -> None:
        pass
