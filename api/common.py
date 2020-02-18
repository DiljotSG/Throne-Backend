from flask import request
from jsonschema import validate


def get_cognito_user():
    event = request.environ.get("serverless.event", "no event")
    # Get the name of the currently authenticated Cognito user
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

    try:
        validate(instance=event, schema=schema)
    except ValidationError:
        return None
    return event.requestContext.authorizer.claims.username
