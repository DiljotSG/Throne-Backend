from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json
from ..persistence import create_user_store

from api.common import get_cognito_user

user_store = create_user_store()


mod = Blueprint('users', __name__)
cors = CORS(mod)


@mod.route("", methods=["GET"])
@cross_origin()
def get_current_user():
    # This is temporary, in the future we will return the user object
    data = {
        "username": get_cognito_user()
    }
    return return_as_json(data)


@mod.route("/<int:user_id>", methods=["GET"])
@cross_origin()
def get_user(user_id):
    return return_as_json(user_store.get_user(user_id))


@mod.route("/<int:user_id>/reviews", methods=["GET"])
@cross_origin()
def get_users_reviews(user_id):
    return return_as_json(user_store.get_reviews_by_user(user_id))


@mod.route("/<int:user_id>/favorites", methods=["GET"])
@cross_origin()
def get_user_favorites(user_id):
    return return_as_json(user_store.get_favorites_by_user(user_id))


@mod.route("/<int:user_id>/favorites", methods=["POST"])
@cross_origin()
def post_user_favorites(user_id):
    return return_as_json({"msg": "Needs to be implemented"})


@mod.route("/<int:user_id>/favorites/<int:favorites_id>", methods=["DELETE"])
@cross_origin()
def delete_user_favorites(user_id, favorites_id):
    return return_as_json({"msg": "Needs to be implemented"})
