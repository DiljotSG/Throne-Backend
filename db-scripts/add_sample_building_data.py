import json
from api.persistence.implementations.amenity_impl import AmenitiesPersistence
from api.persistence.implementations.building_impl import BuildingsPersistence
from api.persistence.implementations.rating_impl import RatingsPersistence
from api.persistence.implementations.washroom_impl import WashroomsPersistence
from api.objects.amenity import Amenity
from api.objects.location import Location


data = None
a = AmenitiesPersistence()
b = BuildingsPersistence()
ra = RatingsPersistence()
w = WashroomsPersistence()

with open('db-scripts/buildings.json') as f:
    data = json.load(f)

buildings = data["buildings"]

for building in buildings:
    best_ratings_id = ra.add_rating(0, 0, 0, 0)
    buildingID = b.add_building(
        Location(
            building["location"]["latitude"],
            building["location"]["longitude"]
        ),
        building["title"],
        building["map_service_id"],
        building["overall_rating"],
        best_ratings_id
    )
    print(f"Added building #{buildingID}")

# Add two (REAL!) washrooms
# Use the University Centre and the Elizabeth Dafoe Library
u_centre = buildings[1]
amenity0 = a.add_amenities(
    Amenity.AUTO_DRYER, Amenity.PAPER_TOWEL,
    Amenity.CONTRACEPTION, Amenity.GARBAGE_CAN
)
rating0 = ra.add_rating(0, 0, 0, 0)

w.add_washroom(
    u_centre["id"],
    Location(
        u_centre["location"]["latitude"],
        u_centre["location"]["longitude"]
    ),
    "University Centre Main Floor Washroom",
    2,
    "men",
    amenity0,
    0,
    rating0
)
print("Added U Centre washroom")

dafoe = buildings[9]
amenity1 = a.add_amenities(
    Amenity.AIR_DRYER,
    Amenity.AUTO_SINK,
    Amenity.BRAILLE_LABELING,
    Amenity.COAT_HOOK,
    Amenity.GARBAGE_CAN,
    Amenity.PAPER_TOWEL,
    Amenity.SAFETY_RAIL,
    Amenity.WHEEL_CHAIR_ACCESS,
)
rating1 = ra.add_rating(0, 0, 0, 0)

w.add_washroom(
    dafoe["id"],
    Location(
        dafoe["location"]["latitude"],
        dafoe["location"]["longitude"]
    ),
    "Elizabeth Dafoe Library Main Floor Washroom",
    2,
    "men",
    amenity1,
    0,
    rating1
)
print("Added Dafoe Library washroom")
print("Done!")
