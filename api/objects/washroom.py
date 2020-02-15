class Washroom:
    def __init__(self,
                 washroom_id,
                 title,
                 location,
                 created_at,
                 gender,
                 floor,
                 building_ID,
                 overall_rating):
        self.washroom_id = washroom_id
        self.title = title
        self.location = location
        self.created_at = created_at
        self.gender = gender
        self.floor = floor
        self.building_ID = building_ID
        self.overall_rating = overall_rating

        self.average_ratings = []
        self.amenities = []
