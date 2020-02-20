from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_cors import cross_origin
from flask.json import JSONEncoder

from datetime import datetime, date, timezone

from api.common import return_as_json
from api.routes.root import root_data
from api.routes.root import mod as root_mod
from api.routes.washrooms import mod as washrooms_mod
from api.routes.buildings import mod as buildings_mod
from api.routes.reviews import mod as reviews_mod
from api.routes.users import mod as users_mod


# Custom JSON Encoder to enforce isoformat for datetime
class ThroneJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            fixed_dt = o.replace(microsecond=0).replace(tzinfo=timezone.utc)
            return fixed_dt.isoformat()
        elif isinstance(o, date):
            fixed_d = o.replace(microsecond=0).replace(tzinfo=timezone.utc)
            return fixed_d.isoformat()

        return super().default(o)


# We do this so that the Flask application isn't strict about trailing slashes
class ThroneFlask(Flask):
    json_encoder = ThroneJSONEncoder

    def add_url_rule(self, *args, **kwargs):
        if 'strict_slashes' not in kwargs:
            kwargs['strict_slashes'] = False
        super(ThroneFlask, self).add_url_rule(*args, **kwargs)


def create():
    app = ThroneFlask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app)

    # Register blueprint routes
    app.register_blueprint(root_mod, url_prefix="/")
    app.register_blueprint(washrooms_mod, url_prefix="/washrooms")
    app.register_blueprint(buildings_mod, url_prefix="/buildings")
    app.register_blueprint(reviews_mod, url_prefix="/reviews")
    app.register_blueprint(users_mod, url_prefix="/users")

    # Get a map of all the endpoints for the root endpoint
    data = root_data()
    data["endpoints"] = []
    for rule in app.url_map.iter_rules():
        data["endpoints"].append(str(rule))

    # Establish the root endpoint
    @app.route("/")
    @cross_origin()
    def root():
        return return_as_json(data)

    return app
