from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json
from ..persistence import create_user_store

from api.common import get_cognito_user

user_store = create_user_store()


mod = Blueprint('users', __name__)
cors = CORS(mod)


@mod.route("")
@cross_origin()
def current_user():
    # This is temporary, in the future we will return the user object
    data = {
        "username": get_cognito_user()
    }
    return return_as_json(data)


@mod.route("/<int:user_id>")
@cross_origin()
def user(user_id):
    return return_as_json(user_store.get_user(user_id))


@mod.route("/<int:user_id>/reviews")
@cross_origin()
def users_reviews(user_id):
    return return_as_json(user_store.get_reviews_by_user(user_id))


@mod.route("/<int:user_id>/favorites")
@cross_origin()
def users_favorites(user_id):
    return return_as_json(user_store.get_favorites_by_user(user_id))
