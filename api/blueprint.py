from flask import jsonify
from flask import Blueprint
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin

from .objects.washrooms import Washroom

api = Blueprint('admin', __name__)
cors = CORS(api)
washroom = Washroom()

@api.route("/washrooms")
@cross_origin()
def washrooms():
    return "washrooms"

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

@api.route("/")
@cross_origin()
def get_washroom_list():
    return jsonify(washroom.get_list())
