from flask import request
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json
from api.response_codes import HttpCodes
from ..objects.location import Location
from ..persistence import create_building_store
from ..persistence import create_washroom_store

building_store = create_building_store()
washroom_store = create_washroom_store()


mod = Blueprint('buildings', __name__)
cors = CORS(mod)


@mod.route("", methods=["GET"])
@cross_origin()
def get_buildings():
    result = None
    code = HttpCodes.HTTP_200_OK

    try:
        # Try to get the URL parameters
        lat = request.args.get("latitude", type=float)
        long = request.args.get("longitude", type=float)
        radius = request.args.get("radius", type=float)
        max_results = request.args.get("max_results", type=int)
        amenities = request.args.get("amenities", type=str)

        # Parse lat and long into a Location object
        location = None
        if lat and long:
            location = Location(lat, long)

        # Parse the amenities into a comma seperated list
        if amenities:
            amenities = amenities.split(",")

        # Don't waste resources if they want nothing back
        if max_results and max_results <= 0:
            result = []
            return return_as_json(result, code)

        result = building_store.get_buildings(
            location,
            radius,
            max_results,
            amenities
        )
    except ValueError:
        code = HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY

    return return_as_json(result, code)


@mod.route("/<int:building_id>", methods=["GET"])
@cross_origin()
def buildings_id(building_id):
    return return_as_json(building_store.get_building(building_id))


@mod.route("/<int:building_id>/washrooms", methods=["GET"])
@cross_origin()
def building_washrooms(building_id):
    return return_as_json(
        washroom_store.get_washrooms_by_building(building_id)
    )
