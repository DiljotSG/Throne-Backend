from flask import jsonify
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin

main_api = Blueprint('admin', __name__)
cors = CORS(main_api)


@main_api.route("/")
@cross_origin()
def get_washroom_list():
    my_list = [
        "Tache Hall",
        "6th Floor E2",
        "Aaron's House",
        "151 Research",
        "University Center",
        "McDonald's Kenaston",
        "3rd Floor Science and Technology Library",
        "Wendy's Kenaston",
        "Armes Tunnel Level",
        "Eric's House",
        "Tyler's House",
        "University College Tunnel Level"
    ]

    return jsonify(my_list)
