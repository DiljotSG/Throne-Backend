from flask import request
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json
from ..objects.location import Location
from ..persistence import create_washroom_store

washroom_store = create_washroom_store()


mod = Blueprint('washrooms', __name__)
cors = CORS(mod)


@mod.route("")
@cross_origin()
def washrooms():
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


@mod.route("/<int:washroom_id>")
@cross_origin()
def washrooms_id(washroom_id):
    return return_as_json(washroom_store.get_washroom(washroom_id))


@mod.route("/<int:washroom_id>/reviews")
@cross_origin()
def washrooms_reviews(washroom_id):
    return return_as_json(washroom_store.get_reviews_by_washrooms(washroom_id))
