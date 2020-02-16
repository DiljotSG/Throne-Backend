from abc import ABC
from abc import abstractmethod


class IWashroomsPersistence(ABC):

    @abstractmethod
    def add_washroom(
        self,
        building_id,  # Foreign Key
        location,
        title,
        floor,
        gender,
        amenities_id,  # Foreign Key
        overall_rating,
        average_ratings_id  # Foreign Key
    ):
        # Return Washroom id
        pass

    @abstractmethod
    def remove_washroom(
        self,
        washroom_id
    ):
        # Cascase delete amenities table entry
        # Cascase delete average ratings table entry
        pass


class IBuildingsPersistence(ABC):
    @abstractmethod
    def add_building(
        self,
        location,
        title,
        map_service_id,
        overall_rating,
    ):
        # Return Building id
        pass

    @abstractmethod
    def remove_building(
        self,
        building_id
    ):
        pass


class IReviewsPersistence(ABC):
    @abstractmethod
    def add_review(
        self,
        washroom_id,  # Foreign Key
        user_id,  # Foreign Key
        rating_id,  # Foreign Key
        comment,
        upvote_count
    ):
        # Return Review id
        pass

    @abstractmethod
    def remove_review(
        self,
        review_id
    ):
        pass


class IRatingsPersistence(ABC):
    @abstractmethod
    def add_rating(
        self,
        cleanliness,
        privacy,
        smell,
        toilet_paper_ply,
    ):
        # Return Rating id
        pass

    @abstractmethod
    def remove_rating(
        self,
        rating_id
    ):
        pass


class IAmenitiesPersistence(ABC):
    @abstractmethod
    def add_amenity(
        self,
        *amenities
    ):
        # Return Amenity id
        pass

    @abstractmethod
    def remove_amenity(
        self,
        amenity_id
    ):
        pass


class IFavoritesPersistence(ABC):
    @abstractmethod
    def add_favorite(
        self,
        user_id,
        washroom_id
    ):
        # Return Favorite id
        pass

    @abstractmethod
    def remove_favorite(
        self,
        favorite_id
    ):
        pass


class IPreferencesPersistence(ABC):
    @abstractmethod
    def add_preference(
        self,
        gender,
        wheelchair_accessible,
        main_floor_access
    ):
        # Return Preference id
        pass

    @abstractmethod
    def remove_preference(
        self,
        preference_id
    ):
        pass
