class Washroom:
    def __init__(
        self,
        washroom_id,
        title,
        location,
        created_at,
        gender,
        floor,
        building_id,
        overall_rating,
        average_rating_id,
        amenities_id
    ):
        self.id = washroom_id
        self.title = title
        self.location = location
        self.created_at = created_at
        self.gender = gender
        self.floor = floor
        self.building_id = building_id
        self.overall_rating = overall_rating
        self.average_rating_id = average_rating_id
        self.amenities_id = amenities_id
