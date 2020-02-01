from flask import Flask
from api.blueprint import main_api

app = Flask(__name__)
app.register_blueprint(main_api, url_prefix='/')


def main():
    app.run()


if __name__ == "__main__":
    main()
