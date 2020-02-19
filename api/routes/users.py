from flask import jsonify
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from ..persistence import create_user_store

user_store = create_user_store


mod = Blueprint('users', __name__)
cors = CORS(mod)


@mod.route("/<int:user_id>")
@cross_origin()
def user(user_id):
    return jsonify({"msg": "user: " + str(user_id)})


@mod.route("/<int:user_id>/reviews")
@cross_origin()
def users_reviews(user_id):
    return jsonify({"msg": "reviews from user: " + str(user_id)})


@mod.route("/<int:user_id>/favorites")
@cross_origin()
def users_favorites(user_id):
    return jsonify({"msg": "favorites of user: " + str(user_id)})
