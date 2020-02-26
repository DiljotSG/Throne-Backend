class Building:
    def __init__(
        self,
        building_id,
        location,
        title,
        maps_service_id,
        created_at,
        overall_rating,
        best_rating_id
    ):
        self.id = building_id
        self.location = location
        self.maps_service_id = maps_service_id
        self.title = title
        self.created_at = created_at
        self.overall_rating = overall_rating
        self.best_rating_id = best_rating_id
