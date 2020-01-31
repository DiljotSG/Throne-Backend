from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route("/")
def washrooms():
    return jsonify([
            "Tache Hall",
            "6th Floor E2",
            "Aaron's House",
            "151 Research",
            "University Center",
            "McDonald's Kenaston",
            "3rd Floor Science and Technology Library",
            "Wendy's Kenaston",
            "Armes Tunnel Level",
            "Eric's House",
            "Tyler's House",
            "University College Tunnel Level"
        ])


def main():
    app.run()


if __name__ == "__main__":
    main()
