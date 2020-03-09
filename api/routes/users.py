from flask import Blueprint
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin

from api.common import return_as_json
from api.common import return_error
from api.common import return_no_content
from api.common import return_not_found
from api.response_codes import HttpCodes
from ..exceptions.throne_exception import ThroneException
from ..exceptions.throne_unauthorized_exception import \
    ThroneUnauthorizedException
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


@mod.route("/reviews", methods=["GET"])
@cross_origin()
def get_reviews():
    return return_as_json(user_store.get_reviews())


@mod.route("/<int:user_id>/reviews", methods=["GET"])
@cross_origin()
def get_users_reviews(user_id):
    return return_as_json(user_store.get_reviews_by_user(user_id))


@mod.route("/favorites", methods=["GET"])
@cross_origin()
def get_user_favorites():
    return return_as_json(user_store.get_favorites())


@mod.route("/favorites", methods=["POST"])
@cross_origin()
def post_user_favorites():
    result = None

    # Don't accept garbage input
    if request.json is None:
        return return_error()

    try:
        washroom_id = 0
        if "washroom_id" in request.json:
            washroom_id = int(request.json["washroom_id"])
        else:
            # If we don't get washroom_id, look for id
            washroom_id = int(request.json["id"])

        result = user_store.add_favorite(
            washroom_id
        )

    except ThroneException as e:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    except ValueError:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY)
    except KeyError:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    return return_as_json(result, HttpCodes.HTTP_201_CREATED)


@mod.route("/favorites", methods=["DELETE"])
@cross_origin()
def delete_user_favorites():
    result = False

    # Don't accept garbage input
    if request.json is None:
        return return_error()

    try:
        washroom_id = 0
        if "washroom_id" in request.json:
            washroom_id = int(request.json["washroom_id"])
        else:
            # If we don't get washroom_id, look for id
            washroom_id = int(request.json["id"])

        result = user_store.remove_favorite(
            washroom_id
        )

    except ThroneException as e:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    except ValueError:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY)
    except KeyError:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    if not result:
        return return_not_found()

    return return_no_content()


@mod.route("/preferences", methods=["PUT"])
@cross_origin()
def get_preferences():
    result = None

    # Don't accept garbage input
    if request.json is None:
        return return_error()

    try:
        gender = str(request.json["gender"])
        wheelchair_accessible = bool(request.json["wheelchair_accessible"])
        main_floor_access = bool(request.json["main_floor_access"])

        result = user_store.update_preferences(
            gender,
            wheelchair_accessible,
            main_floor_access
        )

    except ThroneUnauthorizedException as e:
        return return_error(HttpCodes.HTTP_403_FORBIDDEN, str(e))
    except ThroneException as e:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    except ValueError:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY)
    except KeyError:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    return return_as_json(result)
