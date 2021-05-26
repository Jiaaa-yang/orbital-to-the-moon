from flask import Flask
from . import home

def create_app():
    app = Flask(__name__)

    app.register_blueprint(home.bp)

    return app