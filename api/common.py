import datetime
from flask import request
from flask import jsonify
from jsonschema import validate
from jsonschema import ValidationError
from math import sin, cos, sqrt, atan2, radians

OK = 200
BAD_REQUEST = 400
timestamp_format = '%Y-%m-%d %H:%M:%S'


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
    if data is None:
        result = {
            "Error": "Invalid Request"
        }
        code = BAD_REQUEST

    return jsonify(result), code


def distance_between_locations(loc1, loc2):
    radius = 6371
    lat1 = radians(loc1.latitude)
    lat2 = radians(loc2.latitude)

    diffLat = radians(loc2.latitude - loc1.latitude)
    diffLon = radians(loc2.longitude - loc1.longitude)

    a = (sin(diffLat/2)**2) + cos(lat1) * cos(lat2) * (sin(diffLon/2)**2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return radius * c


def convert_to_mysql_timestamp(timestamp: datetime):
    return timestamp.strftime(timestamp_format)
