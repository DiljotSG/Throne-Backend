class Washroom:
    def __init__(self,
                 id,
                 title,
                 location,
                 timestamp,
                 gender,
                 floor,
                 building_ID,
                 overall_rating):
        self.id = id
        self.title = title
        self.location = location
        self.timestamp = timestamp
        self.gender = gender
        self.floor = floor
        self.bulding_ID = building_ID
        self.overall_rating = overall_rating

        average_ratings = []
        amenities = []
