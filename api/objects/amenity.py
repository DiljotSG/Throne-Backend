from enum import Enum
from typing import List


class Amenity(str, Enum):
    AIR_DRYER: str = "air_dryer",
    AIR_FRESHENER: str = "air_freshener",
    AUTO_DRYER: str = "auto_dryer",
    AUTO_PAPER_TOWEL: str = "auto_paper_towel",
    AUTO_SINK: str = "auto_sink",
    AUTO_TOILET: str = "auto_toilet",
    BABY_CHANGE_STATION: str = "baby_change_station",
    BABY_POWDER: str = "baby_powder",
    BATHROOM_ATTENDANT: str = "bathroom_attendant ",
    BIDET: str = "bidet",
    BODY_TOWEL: str = "body_towel",
    BODYWASH: str = "bodywash",
    BRAILLE_LABELING: str = "braille_labeling",
    CALL_BUTTON: str = "call_button",
    COAT_HOOK: str = "coat_hook",
    CONTRACEPTION: str = "contraception",
    DIAPERS: str = "diapers",
    HYGIENE_PRODUCTS: str = "hygiene_products",
    FIRST_AID: str = "first_aid",
    FULL_BODY_MIRROR: str = "full_body_mirror",
    GARBAGE_CAN: str = "garbage_can",
    HEATED_SEAT: str = "heated_seat",
    LOTION: str = "lotion",
    MOIST_TOWELETTE: str = "moist_towelette",
    MUSIC: str = "music",
    NEEDLE_DISPOSAL: str = "needle_disposal",
    PAPER_SEAT_COVERS: str = "paper_seat_covers",
    PAPER_TOWEL: str = "paper_towel",
    PERFUME_COLOGNE: str = "perfume_cologne",
    SAFETY_RAIL: str = "safety_rail",
    SAUNA: str = "sauna",
    SHAMPOO: str = "shampoo",
    SHOWER: str = "shower",
    TISSUES: str = "tissues",
    WHEEL_CHAIR_ACCESS: str = "wheel_chair_access"

    @staticmethod
    def verify_list(amenities: List[str]):
        # TODO: Add support for verifying if a list of strings
        # of contains all valid Amenities
        return True
