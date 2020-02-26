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

    # Try to get the URL parameters as floats
    # TODO: Provide a way for the client to pass in desired amenities
    try:
        lat = request.args.get("latitude")
        long = request.args.get("longitude")
        radius = request.args.get("radius")

        if lat is None or long is None:
            result = building_store.get_buildings()
        else:
            result = building_store.get_buildings(
                Location(
                    float(lat),
                    float(long)
                ),
                float(radius),
            )
    except ValueError:
        pass

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
