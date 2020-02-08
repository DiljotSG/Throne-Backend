from flask import jsonify
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin

mod = Blueprint('reviews', __name__)
cors = CORS(mod)


@mod.route("/<int:review_id>")
@cross_origin()
def reviews_id(review_id):
    return jsonify({"msg": "review: " + str(review_id)})
