from flask import Flask
from api.blueprint import main_api

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(main_api, url_prefix='/')


def main():
    app.run()


if __name__ == "__main__":
    main()
