from flask import jsonify
from flask import Blueprint

from .washrooms import Washroom

main_api = Blueprint('admin', __name__)
washroom = Washroom()


@main_api.route("/")
def get_washroom_list():
    return jsonify(washroom.get_list())
