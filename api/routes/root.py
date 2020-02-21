from flask import request
from flask import Blueprint
from flask_cors import CORS
from flask_cors import cross_origin
from api.common import return_as_json

from api.common import get_cognito_user

mod = Blueprint('root', __name__)
cors = CORS(mod)


# This is some of the information returned at the root endpoint
# The root endpoint is established in ../__init__.py
def root_data():
    data = {
        "data": "Welcome to the Throne API."
    }
    return data


@mod.route("/user")
@cross_origin()
def current_user():
    # This is temporary, in the future we will return the user object
    data = {
        "username": get_cognito_user()
    }
    return return_as_json(data)


@mod.route("/debug")
@cross_origin()
def debug():
    data = {
        "Request-Header": str(request.headers),
        "Request-URL": request.url,
        "Serverless-Context": str(request.environ.get(
            "serverless.context",
            "no context"
        )),
        "Serverless-Event": request.environ.get(
            "serverless.event",
            "no event"
        ),
    }
    return return_as_json(data)
