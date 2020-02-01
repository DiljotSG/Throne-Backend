from flask import jsonify
from flask import Blueprint
from flask_cors import CORS
from flash import cross_origin

from .objects.washrooms import Washroom

main_api = Blueprint('admin', __name__)
cors = CORS(main_api)
washroom = Washroom()


@main_api.route("/")
@cross_origin()
def get_washroom_list():
    return jsonify(washroom.get_list())
