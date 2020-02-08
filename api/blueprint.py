from flask import jsonify
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin

from .objects.washroom import Washroom

main_api = Blueprint('admin', __name__)
cors = CORS(main_api)
washroom = Washroom(0, "washroom", "EITC 2", "0", "male", 1, 1, 5)


@main_api.route("/")
@cross_origin()
def get_washroom_list():
    return jsonify(washroom.title, washroom.location, washroom.gender)
