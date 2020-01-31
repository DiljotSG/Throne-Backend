from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route("/")
def washrooms():
    return jsonify({
        "washrooms": [
            "Tache Hall",
            "6th Floor E2",
            "Aaron's House",
            "151 Research",
            "University Center"
            ]
        })
