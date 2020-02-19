from flask import jsonify
from flask import Blueprint
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin
import persistence

building_store = persistence.create_building_store()


mod = Blueprint('buildings', __name__)
cors = CORS(mod)


@mod.route("/")
@cross_origin()
def buildings():
    location = request.args.get("location")
    return jsonify({"msg": "building at location = " + str(location)})


@mod.route("/<int:building_id>")
@cross_origin()
def buildings_id(building_id):
    return jsonify({"msg": "building: " + str(building_id)})


@mod.route("/<int:building_id>/washrooms")
@cross_origin()
def building_reviews(building_id):
    return jsonify({"msg": "washrooms in building: " + str(building_id)})
