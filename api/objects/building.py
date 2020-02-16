class Building:
    def __init__(
        self,
        building_id,
        location,
        maps_service_id,
        created_at,
        overall_rating
    ):
        self.id = building_id
        self.location = location
        self.maps_service_id = maps_service_id
        self.created_at = created_at
        self.overall_rating = overall_rating

        self.best_ratings = []
