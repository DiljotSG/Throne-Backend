from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json


mod = Blueprint('preferences', __name__)
cors = CORS(mod)


@mod.route("", methods=["GET"])
@cross_origin()
def get_preferences():
    return return_as_json({"msg": "Needs to be implemented"})
