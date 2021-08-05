from flask import Flask
from os import getenv
from .views import home, analysis


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')

    app.register_blueprint(home.bp)
    app.register_blueprint(analysis.bp)
    app.secret_key = getenv("FLASK_SECRET_KEY")

    return app
