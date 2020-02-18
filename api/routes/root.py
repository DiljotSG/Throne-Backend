from flask import jsonify
from flask import Blueprint
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin
from jsonschema import validate

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
    event = request.environ.get("serverless.event", "no event")
    # Get the name of the currently authenticated Cognito
    # This is temporary, in the future we will return the user obj

    # Make sure our event has the proper data - validate the schema
    schema = {
        "type": "object",
        "requestContext": {
            "type": "object",
            "authorizer": {
                "type": "object",
                "claims": {
                    "type": "object",
                    "username": {
                        "type": "string"
                    }
                }
            }
        }
    }

    if isinstance(event, dict):
        validate(instance=event, schema=schema)
        data = {
            "username": event.requestContext.authorizer.claims.username
        }
        return jsonify(data)
    else:
        # If they aren't logged in, we can't do this.
        return jsonify({
            "message": "Unauthorized"
        }), 401


@mod.route("/debug")
@cross_origin()
def debug():
    data = {
        "Request-Header": str(request.headers),
        "Request-URL": request.url,
        "Serverless-Context": request.environ.get(
            "serverless.context",
            "no context"
        ),
        "Serverless-Event": request.environ.get(
            "serverless.event",
            "no event"
        ),
    }
    return jsonify(data)
