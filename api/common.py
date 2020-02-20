from flask import request
from flask import jsonify
from jsonschema import validate
from jsonschema import ValidationError

OK = 200
BAD_REQUEST = 400


def is_valid_schema(obj, schema):
    result = True
    try:
        validate(instance=obj, schema=schema)
    except ValidationError:
        result = False
    return result


def get_cognito_user():
    # Get the name of the currently authenticated Cognito user
    event = request.environ.get("serverless.event", "no event")

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

    username = None

    # Make sure our event has the proper data - validate the schema
    if is_valid_schema(event, schema):
        username = event["requestContext"]["authorizer"]["claims"]["username"]

    return username


def return_as_json(data):
    result = data
    code = OK

    # If our data is non-existant, this is a bad request.
    if not data:
        result = {
            "Error": "Invalid Request"
        }
        code = BAD_REQUEST

    return jsonify(result), code
