from flask import jsonify
from flask import Blueprint
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin

api = Blueprint('admin', __name__)
cors = CORS(api)

@api.route("/washrooms")
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


@api.route("/washrooms/<int:washroom_id>")
@cross_origin()
def washrooms_id(washroom_id):
    return "washroom: " + str(washroom_id)


@api.route("/washrooms/<int:washroom_id>/reviews")
@cross_origin()
def washrooms_reviews(washroom_id):
    return "reviews for washroom: " + str(washroom_id)


@api.route("/buildings")
@cross_origin()
def buildings():
    location = request.args.get("location")
    return "location = " + str(location)


@api.route("/buildings/<int:building_id>")
@cross_origin()
def buildings_id(building_id):
    return "building: " + str(building_id)


@api.route("/buildings/<int:building_id>/washrooms")
@cross_origin()
def building_reviews(building_id):
    return "washrooms in building: " + str(building_id)


@api.route("/users/<int:user_id>")
@cross_origin()
def user(user_id):
    return "user: " + str(user_id)


@api.route("/users/<int:user_id>/reviews")
@cross_origin()
def users_reviews(user_id):
    return "reviews from user: " + str(user_id)


@api.route("/users/<int:user_id>/favorites")
@cross_origin()
def users_favorites(user_id):
    return "favorites of user: " + str(user_id)
