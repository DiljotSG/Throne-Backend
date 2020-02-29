from flask import request
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json
from api.common import return_error
from api.response_codes import HttpCodes
from ..objects.location import Location
from ..persistence import create_washroom_store
from ..persistence import create_building_store
from ..persistence import create_review_store

from ..exceptions.throne_exception import ThroneException

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
    except (ValueError):
        code = HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY

    return return_as_json(result, code)


@mod.route("", methods=["POST"])
@cross_origin()
def post_washrooms():
    result = None

    try:
        title = str(request.json["title"])
        longitude = float(request.json["location"]["longitude"])
        latitude = float(request.json["location"]["latitude"])
        gender = str(request.json["gender"])
        floor = int(request.json["floor"])
        building_id = int(request.json["building_id"])
        amenities = list(request.json["amenities"])

        result = washroom_store.create_washroom(
            title,
            longitude,
            latitude,
            gender,
            floor,
            building_id,
            amenities
        )

    except ThroneException as e:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY, str(e))

    except ValueError:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY)

    except KeyError:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    return return_as_json(result)


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

    try:
        comment = str(request.json["comment"])
        cleanliness = float(request.json["ratings"]["cleanliness"])
        privacy = float(request.json["ratings"]["privacy"])
        smell = float(request.json["ratings"]["smell"])
        toilet_paper_quality = \
            float(request.json["ratings"]["toilet_paper_quality"])

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

    return return_as_json(result)


@mod.route("/<int:washroom_id>/reviews/<int:review_id>", methods=["PUT"])
@cross_origin()
def put_washroom_review(washroom_id, review_id):
    code = HttpCodes.HTTP_200_OK
    result = None

    try:
        # TODO: get_cognito_user() returns a username, support for
        # retrieving current user's id is required
        # user_name = get_cognito_user()
        user_id = 0
        comment = str(request.json["comment"])
        ratings = list(request.json["ratings"])

        result = review_store.update_review(
            washroom_id,
            user_id,
            comment,
            ratings
        )

    except (ValueError):
        code = HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY

    return return_as_json(result, code)
