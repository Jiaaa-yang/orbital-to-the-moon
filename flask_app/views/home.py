"""
Blueprint for homepage of application
"""
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
