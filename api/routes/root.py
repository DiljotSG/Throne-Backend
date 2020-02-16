from flask import jsonify
from flask import Blueprint
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin

mod = Blueprint('root', __name__)
cors = CORS(mod)


# This is some of the information returned at the root endpoint
# The root endpoint is established in ../__init__.py
def root_data():
    data = {
        "data": "Welcome to the Throne API."
    }
    return data


@mod.route("/debug")
@cross_origin()
def debug():
    my_list = [
        str(request.headers),
        str(request.url),
        str(request.environ.get("serverless.context", "no context")),
        str(request.environ.get("serverless.event", "no event")),
    ]
    return jsonify(my_list)
