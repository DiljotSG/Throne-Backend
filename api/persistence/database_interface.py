from abc import ABC
from abc import abstractmethod


class IWashroomsPersistence(ABC):

    @abstractmethod
    def add_washroom(
        self,
        building_ID,  # Foreign Key
        location,
        title,
        floor,
        gender,
        amenities_ID,  # Foreign Key
        overall_rating,
        average_ratings_ID  # Foreign Key
    ):
        # Return Washroom ID
        pass

    @abstractmethod
    def remove_washroom(
        self,
        washroom_ID
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
        map_service_ID,
        overall_rating,
    ):
        # Return Building ID
        pass

    @abstractmethod
    def remove_building(
        self,
        building_ID
    ):
        pass


class IReviewsPersistence(ABC):
    @abstractmethod
    def add_review(
        self,
        washroom_ID,  # Foreign Key
        user_ID,  # Foreign Key
        rating_ID,  # Foreign Key
        comment,
        upvote_count
    ):
        # Return Review ID
        pass

    @abstractmethod
    def remove_review(
        self,
        review_ID
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
        # Return Rating ID
        pass

    @abstractmethod
    def remove_rating(
        self,
        rating_ID
    ):
        pass


class IAmenitiesPersistence(ABC):
    @abstractmethod
    def add_amenity(
        self,
        *amenities
    ):
        # Return Amenity ID
        pass

    @abstractmethod
    def remove_amenity(
        self,
        amenity_ID
    ):
        pass


class IFavoritesPersistence(ABC):
    @abstractmethod
    def add_favorite(
        self,
        user_ID,
        washroom_ID
    ):
        # Return Favorite ID
        pass

    @abstractmethod
    def remove_favorite(
        self,
        favorite_ID
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
        # Return Preference ID
        pass

    @abstractmethod
    def remove_preference(
        self,
        preference_ID
    ):
        pass
