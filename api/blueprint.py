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
    return jsonify({"msg" : "washroom: " + str(washroom_id)})


@api.route("/washrooms/<int:washroom_id>/reviews")
@cross_origin()
def washrooms_reviews(washroom_id):
    return jsonify({"msg" : "reviews for washroom: " + str(washroom_id)})


@api.route("/reviews/<int:review_id>")
@cross_origin()
def reviews_id(review_id):
    return jsonify({"msg" : "review: " + str(review_id)})


@api.route("/buildings")
@cross_origin()
def buildings():
    location = request.args.get("location")
    return jsonify({"msg" : "building at location = " + str(location)}) 


@api.route("/buildings/<int:building_id>")
@cross_origin()
def buildings_id(building_id):
    return jsonify({"msg" : "building: " + str(building_id)})


@api.route("/buildings/<int:building_id>/washrooms")
@cross_origin()
def building_reviews(building_id):
    return jsonify({"msg" : "washrooms in building: " + str(building_id)})


@api.route("/users/<int:user_id>")
@cross_origin()
def user(user_id):
    return jsonify({"msg" : "user: " + str(user_id)})


@api.route("/users/<int:user_id>/reviews")
@cross_origin()
def users_reviews(user_id):
    return jsonify({"msg" : "reviews from user: " + str(user_id)})


@api.route("/users/<int:user_id>/favorites")
@cross_origin()
def users_favorites(user_id):
    return jsonify({"msg" : "favorites of user: " + str(user_id)})
