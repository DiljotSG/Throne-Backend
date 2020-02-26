from flask import request
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json
from ..objects.location import Location
from ..persistence import create_building_store
from ..persistence import create_washroom_store

building_store = create_building_store()
washroom_store = create_washroom_store()


mod = Blueprint('buildings', __name__)
cors = CORS(mod)


@mod.route("")
@cross_origin()
def buildings():
    result = None

    # Try to get the URL parameters
    lat = request.args.get("latitude", type=float)
    long = request.args.get("longitude", type=float)
    radius = request.args.get("radius", type=float)

    if lat is None or long is None:
        result = building_store.get_buildings()
    else:
        result = building_store.get_buildings(
            Location(
                lat,
                long
            ),
            radius,
        )

    return return_as_json(result)


@mod.route("/<int:building_id>")
@cross_origin()
def buildings_id(building_id):
    return return_as_json(building_store.get_building(building_id))


@mod.route("/<int:building_id>/washrooms")
@cross_origin()
def building_washrooms(building_id):
    return return_as_json(
        washroom_store.get_washrooms_by_building(building_id)
    )
