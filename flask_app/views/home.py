from flask import (
    Blueprint, render_template, request
)
from .analysis import analysis


bp = Blueprint('index', __name__)

@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        ticker = request.form['ticker'].upper()
        return analysis(ticker)

    return render_template('index.html')

@bp.route('/contact', methods=["GET"])
def contact():
    return(render_template('contact.html'))

@bp.route('/about', methods=["GET"])
def about():
    return(render_template('about.html'))

@bp.route('/ai', methods=["GET"])
def ai():
    return(render_template('ai.html'))