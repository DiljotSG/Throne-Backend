from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json
from api.common import return_not_implemented
from ..persistence import create_user_store


user_store = create_user_store()


mod = Blueprint('users', __name__)
cors = CORS(mod)


@mod.route("", methods=["GET"])
@cross_origin()
def get_current_user():
    return return_as_json(user_store.get_current_user())


@mod.route("/<int:user_id>", methods=["GET"])
@cross_origin()
def get_user(user_id):
    return return_as_json(user_store.get_user(user_id))


@mod.route("/<int:user_id>/reviews", methods=["GET"])
@cross_origin()
def get_users_reviews(user_id):
    return return_as_json(user_store.get_reviews_by_user(user_id))


@mod.route("/favorites", methods=["GET"])
@cross_origin()
def get_user_favorites():
    # TODO: Add support for retrieving user by username
    return return_not_implemented()


@mod.route("/favorites", methods=["POST"])
@cross_origin()
def post_user_favorites():
    # TODO: Add support for retrieving user by username
    return return_not_implemented()


@mod.route("/favorites/<int:favorites_id>", methods=["DELETE"])
@cross_origin()
def delete_user_favorites(favorites_id):
    # TODO: Add support for retrieving user by username
    return return_not_implemented()


@mod.route("/preferences", methods=["GET"])
@cross_origin()
def get_preferences():
    # TODO: Add support for retrieving user by username
    return return_not_implemented()
