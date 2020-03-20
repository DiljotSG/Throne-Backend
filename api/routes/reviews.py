from flask import Blueprint
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin

from api.common import return_as_json
from api.common import return_error
from api.common import return_not_implemented
from api.response_codes import HttpCodes
from ..exceptions.throne_exception import ThroneException
from ..exceptions.throne_unauthorized_exception import \
    ThroneUnauthorizedException
from ..persistence import create_review_store

review_store = create_review_store()


mod = Blueprint('reviews', __name__)
cors = CORS(mod)


@mod.route("/<int:review_id>", methods=["GET"])
@cross_origin()
def get_review(review_id):
    return return_as_json(review_store.get_review(review_id))


@mod.route("/<int:review_id>", methods=["PUT"])
@cross_origin()
def put_washroom_review(review_id):
    result = None

    if request.json is None:
        return return_error(HttpCodes.HTTP_400_BAD_REQUEST)

    try:
        comment = str(request.json["comment"])
        cleanliness = int(request.json["ratings"]["cleanliness"])
        privacy = int(request.json["ratings"]["privacy"])
        smell = int(request.json["ratings"]["smell"])
        toilet_paper_quality = \
            int(request.json["ratings"]["toilet_paper_quality"])

        result = review_store.update_review(
            review_id,
            comment,
            cleanliness,
            privacy,
            smell,
            toilet_paper_quality
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


@mod.route("/<int:review_id>", methods=["DELETE"])
@cross_origin()
def delete_washroom_review(review_id):
    return return_not_implemented()
