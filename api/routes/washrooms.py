from flask import Blueprint
from flask_cors import CORS
from flask import request
from flask_cors import cross_origin
from api.common import return_as_json
from ..persistence import create_washroom_store

washroom_store = create_washroom_store()


mod = Blueprint('washrooms', __name__)
cors = CORS(mod)


@mod.route("")
@cross_origin()
def washrooms():
    location = request.args.get("location")
    return return_as_json(washroom_store.get_washrooms(location))


@mod.route("/<int:washroom_id>")
@cross_origin()
def washrooms_id(washroom_id):
    return return_as_json(washroom_store.get_washroom(washroom_id))


@mod.route("/<int:washroom_id>/reviews")
@cross_origin()
def washrooms_reviews(washroom_id):
    return return_as_json(washroom_store.get_washroom_reviews(washroom_id))
