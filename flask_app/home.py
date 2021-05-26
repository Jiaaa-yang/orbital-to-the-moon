from flask import (
    Blueprint, redirect, render_template, request, url_for
)

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        ticker = request.form['ticker']
        print(ticker)
        return redirect(url_for('main.result'))

    return render_template('index.html')


@bp.route('/results')
def result():
    return render_template('results.html')