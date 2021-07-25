"""Runner module to start flask application

"""
# from dotenv import load_dotenv
# load_dotenv()
from flask_app import create_app
from flask import session


app = create_app()

@app.before_first_request
def make_session_permanent():
    session.permanent = True

# app.run()
