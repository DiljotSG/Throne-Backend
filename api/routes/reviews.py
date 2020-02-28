from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json
from api.common import return_no_content
from ..persistence import create_review_store

review_store = create_review_store()


mod = Blueprint('reviews', __name__)
cors = CORS(mod)


@mod.route("/<int:review_id>", methods=["GET"])
@cross_origin()
def get_review(review_id):
    return return_as_json(review_store.get_review(review_id))


@mod.route("/<int:review_id>", methods=["DELETE"])
@cross_origin()
def delete_review(review_id):
    review_store.delete_review(review_id)
    return return_no_content()
