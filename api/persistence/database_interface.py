from abc import ABC
from abc import abstractmethod


class IWashrooms(ABC):

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


class IBuildings(ABC):
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


class IReviews(ABC):
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


class IRatings(ABC):
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


class IAmenities(ABC):
    @abstractmethod
    def add_amenity(
        self,
        paper_towel=False,
        air_dryer=False,
        soap=False,
        wheelchair_accessible=False,
        automatic_equipment=False,
        shower=False,
        urinal=False,
        paper_seat_covers=False,
        hygiene_products=False,
        needle_disposal=False,
        contraception=False,
        bathroom_attendent=False,
        perfume_colonge=False,
        lotion=False
    ):
        # Return Amenity ID
        pass

    @abstractmethod
    def remove_amenity(
        self,
        amenity_ID
    ):
        pass


class IFavorites(ABC):
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


class IPreferences(ABC):
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
