from flask import Flask
app = Flask(__name__)


@app.route("/")
def washrooms():
    return {
        "washrooms": [
            "Tache Hall",
            "6th Floor E2",
            "Aaron's House",
            "151 Research",
            "University Center"
            ]
        }
