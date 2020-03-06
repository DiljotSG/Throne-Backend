import datetime
import os
from math import sin, cos, sqrt, atan2, radians
from typing import Optional

from flask import jsonify
from flask import request
from jsonschema import ValidationError
from jsonschema import validate

from api.objects.location import Location
from .response_codes import HttpCodes

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


def should_use_db():
    return (os.environ.get("IS_LAMBDA") or os.environ.get("THRONE_USE_DB"))\
        and not (os.environ.get("THRONE_NO_DB_CREDS"))


def is_valid_schema(obj, schema: dict) -> bool:
    result = True
    try:
        validate(instance=obj, schema=schema)
    except ValidationError:
        result = False
    return result


# Get the name of the currently authenticated Cognito user
def get_cognito_user() -> Optional[str]:
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


def return_error(
    code: int = HttpCodes.HTTP_400_BAD_REQUEST,
    message: str = "Invalid Request"
):
    message = str({"Error": message})
    return jsonify(message), code


def return_as_json(data, code=HttpCodes.HTTP_200_OK):
    result = data

    # If our data is non-existant, this is a bad request.
    if data is None:
        return return_error()

    return jsonify(result), code


def return_no_content():
    return "", HttpCodes.HTTP_204_NO_CONTENT


def return_not_implemented():
    return "", HttpCodes.HTTP_501_NOT_IMPLEMENTED


# Returns distance in kilometers
def distance_between_locations(loc1: Location, loc2: Location) -> float:
    radius = 6371
    lat1 = radians(loc1.latitude)
    lat2 = radians(loc2.latitude)

    diffLat = radians(loc2.latitude - loc1.latitude)
    diffLon = radians(loc2.longitude - loc1.longitude)

    a = (sin(diffLat/2)**2) + cos(lat1) * cos(lat2) * (sin(diffLon/2)**2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return radius * c


def convert_to_mysql_timestamp(timestamp: datetime.date):
    return timestamp.strftime(TIMESTAMP_FORMAT)


def verify_gender(gender: str) -> bool:
    gender = gender.lower()
    return gender == "women" or gender == "men" or gender == "all"
