from flask import jsonify
from flask import Blueprint
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin

mod = Blueprint('washrooms', __name__)
cors = CORS(mod)


@mod.route("/")
@cross_origin()
def washrooms():
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


@mod.route("/<int:washroom_id>")
@cross_origin()
def washrooms_id(washroom_id):
    return jsonify({"msg": "washroom: " + str(washroom_id)})


@mod.route("/<int:washroom_id>/reviews")
@cross_origin()
def washrooms_reviews(washroom_id):
    return jsonify({"msg": "reviews for washroom: " + str(washroom_id)})


@mod.route("/debug")
@cross_origin()
def debug():
    my_list = [
        str(request.headers),
        str(request.url),
        str(request.environ.get("serverless.context", "no context")),
        str(request.environ.get("serverless.event", "no event")),
    ]
    return jsonify(my_list)
