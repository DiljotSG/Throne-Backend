from enum import Enum


class Amenity(str, Enum):
    PAPER_TOWEL: str = "Paper Towel"
    AIR_DRYER: str = "Air Dryer"
    SOAP: str = "Soap"
    WHEELCHAIR_ACCESSIBLE: str = "Wheelchair Accessible"
    AUTOMATIC_SINK: str = "Automatic Sink"
    AUTOMATIC_TOILET: str = "Automatic Toilet"
    AUTOMATIC_PAPER_TOWEL: str = "Automatic Paper Towel"
    AUTOMATIC_DRYER: str = "Automatic Dryer"
    SHOWER: str = "Shower"
    URINAL: str = "Urinal"
    PAPER_SEAT_COVERS: str = "Paper Seat Covers"
    HYGIENE_PRODUCTS: str = "Hygiene Products"
    NEEDLE_DISPOSAL: str = "Needle Disposal"
    CONTRACEPTION: str = "Contraception"
    BATHROOM_ATTENDANT: str = "Bathroom Attendant"
    PERFUME_COLOGNE: str = "Perfume/Cologne"
    LOTION: str = "Lotion"
