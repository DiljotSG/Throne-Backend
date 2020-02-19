from flask import jsonify
from flask import request
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from ..persistence import create_building_store

building_store = create_building_store()


mod = Blueprint('buildings', __name__)
cors = CORS(mod)


@mod.route("")
@cross_origin()
def buildings():
    location = request.args.get("location")
    return jsonify(building_store.get_buildings(location))


@mod.route("/<int:building_id>")
@cross_origin()
def buildings_id(building_id):
    return jsonify(building_store.get_building(building_id))


@mod.route("/<int:building_id>/washrooms")
@cross_origin()
def building_reviews(building_id):
    return jsonify(building_store.get_building_reviews(building_id))
