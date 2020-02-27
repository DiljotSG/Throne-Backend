from flask import request
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json
from api.response_codes import HttpCodes
from ..objects.location import Location
from ..persistence import create_washroom_store
from ..persistence import create_building_store
from ..persistence import create_review_store
from api.common import get_cognito_user

washroom_store = create_washroom_store()
building_store = create_building_store()
review_store = create_review_store()


mod = Blueprint('washrooms', __name__)
cors = CORS(mod)


@mod.route("", methods=["GET"])
@cross_origin()
def get_washrooms():
    result = None

    # Try to get the URL parameters as floats
    lat = request.args.get("latitude", type=float)
    long = request.args.get("longitude", type=float)
    radius = request.args.get("radius", type=float)

    if lat is None or long is None:
        result = washroom_store.get_washrooms()
    else:
        result = washroom_store.get_washrooms(
            Location(
                lat,
                long
            ),
            radius,
        )

    return return_as_json(result)


@mod.route("", methods=["POST"])
@cross_origin()
def post_washrooms():
    code = HttpCodes.HTTP_201_CREATED
    result = None

    try:
        title = str(request.json["title"])
        longitude = float(request.json["location"]["longitude"])
        latitude = float(request.json["location"]["longitude"])
        gender = str(request.json["gender"])
        floor = int(request.json["floor"])
        building_id = int(request.json["building_id"])
        amenities = list(request.json["amenities"])

        result = washroom_store.create(
            title,
            longitude,
            latitude,
            gender,
            floor,
            building_id,
            amenities
        )

    except (Exception):
        code = HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY

    return return_as_json(result, code)


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
    code = HttpCodes.HTTP_201_CREATED
    result = None

    try:
        user_id = get_cognito_user()
        comment = str(request.json["comment"])
        ratings = list(request.json["ratings"])

        result = review_store.create(
            washroom_id,
            user_id,
            comment,
            ratings
        )

    except (Exception):
        code = HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY

    return return_as_json(result, code)


@mod.route("/<int:washroom_id>/reviews/<int:review_id>", methods=["PUT"])
@cross_origin()
def put_washroom_review(washroom_id, review_id):
    code = HttpCodes.HTTP_200_OK
    result = None

    try:
        user_id = get_cognito_user()
        comment = str(request.json["comment"])
        ratings = list(request.json["ratings"])

        result = review_store.update(
            washroom_id,
            user_id,
            comment,
            ratings
        )

    except (Exception):
        code = HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY

    return return_as_json(result, code)
