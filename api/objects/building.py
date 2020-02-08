class Building:
    def __init__(self,
                 id,
                 location,
                 maps_service_ID,
                 timestamp,
                 overall_rating,
                 best_ratings):
        self.id = id
        self.location = location
        self.maps_service_ID = maps_service_ID
        self.timestamp = timestamp
        self.overall_rating = overall_rating
        self.best_ratings = best_ratings
