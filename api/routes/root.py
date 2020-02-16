from flask import jsonify
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin

mod = Blueprint('root', __name__)
cors = CORS(mod)


@mod.route("/")
@cross_origin()
def root():
    data = {
        "data": "Welcome to the Throne API."
    }
    return jsonify(data)
