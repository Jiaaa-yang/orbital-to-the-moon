from flask import Flask
from . import home

def create_app():
    app = Flask(__name__)

    #Throwaway secret key; use environment variables or config files locally
    app.secret_key = 'W84Ngvr4mfhyb20ga2lja3MgYXNz'

    app.register_blueprint(home.bp)

    return app
