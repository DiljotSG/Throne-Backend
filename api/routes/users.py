from flask import request
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json
from api.common import return_error
from api.common import return_no_content
from api.response_codes import HttpCodes
from ..persistence import create_user_store
from ..exceptions.throne_exception import ThroneException
from ..exceptions.throne_unauthorized_exception import\
    ThroneUnauthorizedException

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
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    try:
        washroom_id = int(request.json["washroom_id"])

        result = user_store.add_favorite(
            washroom_id
        )

    except ThroneException as e:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    except ValueError:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY)
    except KeyError:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    return return_as_json(result)


@mod.route("/favorites", methods=["DELETE"])
@cross_origin()
def delete_user_favorites():
    # Don't accept garbage input
    if request.json is None:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    try:
        washroom_id = int(request.json["washroom_id"])

        user_store.remove_favorite(
            washroom_id
        )

    except ThroneException as e:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
    except ValueError:
        return return_error(HttpCodes.HTTP_422_UNPROCESSABLE_ENTITY)
    except KeyError:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    return return_no_content()


@mod.route("/preferences", methods=["PUT"])
@cross_origin()
def get_preferences():
    result = None

    # Don't accept garbage input
    if request.json is None:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

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
