import json
from api.persistence.implementations.building_impl import BuildingsPersistence
from api.persistence.implementations.rating_impl import RatingsPersistence
from api.objects.location import Location
from datetime import datetime


data = None

b = BuildingsPersistence()
ra = RatingsPersistence()

with open('db-scripts/buildings.json') as f:
    data = json.load(f)

buildings = data["buildings"]

for building in buildings:
    best_ratings_id = ra.add_rating(0, 0, 0, 0)
    building = b.add_building(
        Location(
            building["location"]["latitude"],
            building["location"]["longitude"]
        ),
        building["title"],
        building["map_service_id"],
        datetime.now(),
        building["overall_rating"],
        best_ratings_id
    )

print("Done!")
