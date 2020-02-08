from flask import Flask

from api.routes.washrooms import mod as washrooms_mod
from api.routes.buildings import mod as buildings_mod
from api.routes.reviews import mod as reviews_mod
from api.routes.users import mod as users_mod

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(washrooms_mod, url_prefix="/washrooms")
app.register_blueprint(buildings_mod, url_prefix="/buildings")
app.register_blueprint(reviews_mod, url_prefix="/reviews")
app.register_blueprint(users_mod, url_prefix="/users")


def main():
    app.run()


if __name__ == "__main__":
    main()
