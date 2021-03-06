from flask import Blueprint
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin

from api.common import return_as_json
from api.common import return_error
from api.response_codes import HttpCodes
from ..exceptions.throne_exception import ThroneException
from ..objects.location import Location
from ..persistence import create_building_store
from ..persistence import create_review_store
from ..persistence import create_washroom_store

washroom_store = create_washroom_store()
building_store = create_building_store()
review_store = create_review_store()


mod = Blueprint('washrooms', __name__)
cors = CORS(mod)


@mod.route("", methods=["GET"])
@cross_origin()
def get_washrooms():
    result = None
    code = HttpCodes.HTTP_200_OK

    try:
        lat = request.args.get("latitude", type=float)
        long = request.args.get("longitude", type=float)
        radius = request.args.get("radius", type=float)
        max_results = request.args.get("max_results", type=int)
        amenities = request.args.get("amenities", type=str)

        location = None
        if lat and long:
            location = Location(lat, long)

        if amenities:
            amenities = amenities.split(",")

        if max_results and max_results <= 0:
            result = []
            return return_as_json(result, code)

        result = washroom_store.get_washrooms(
            location,
            radius,
            max_results,
            amenities
        )
    except ValueError:
        code = HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY

    return return_as_json(result, code)


@mod.route("", methods=["POST"])
@cross_origin()
def post_washrooms():
    result = None

    if request.json is None:
        return return_error()

    try:
        comment = str(request.json["comment"])
        longitude = float(request.json["location"]["longitude"])
        latitude = float(request.json["location"]["latitude"])
        gender = str(request.json["gender"])
        floor = int(request.json["floor"])
        urinal_count = int(request.json["urinal_count"])
        stall_count = int(request.json["stall_count"])
        building_id = int(request.json["building_id"])
        amenities = list(request.json["amenities"])

        result = washroom_store.create_washroom(
            comment,
            longitude,
            latitude,
            gender,
            floor,
            urinal_count,
            stall_count,
            building_id,
            amenities
        )

    except ThroneException as e:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    except ValueError:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY)
    except KeyError:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    return return_as_json(result, HttpCodes.HTTP_201_CREATED)


@mod.route("/<int:washroom_id>", methods=["GET"])
@cross_origin()
def get_washrooms_id(washroom_id):
    return return_as_json(washroom_store.get_washroom(washroom_id))


@mod.route("/<int:washroom_id>/reviews", methods=["GET"])
@cross_origin()
def get_washrooms_reviews(washroom_id):
    return return_as_json(washroom_store.get_reviews_by_washrooms(washroom_id))


@mod.route("/<int:washroom_id>/reviews", methods=["POST"])
@cross_origin()
def post_washrooms_reviews(washroom_id):
    result = None

    if request.json is None:
        return return_error()

    try:
        if "comment" in request.json:
            comment = str(request.json["comment"])
        else:
            comment = ""
        cleanliness = int(request.json["ratings"]["cleanliness"])
        privacy = int(request.json["ratings"]["privacy"])
        smell = int(request.json["ratings"]["smell"])
        toilet_paper_quality = int(request.json["ratings"]["toilet_paper_quality"])

        result = review_store.create_review(
            washroom_id,
            comment,
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
        )

    except ThroneException as e:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    except ValueError:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY)
    except KeyError:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    return return_as_json(result, HttpCodes.HTTP_201_CREATED)
