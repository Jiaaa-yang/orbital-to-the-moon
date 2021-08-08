from flask import (
    Blueprint, render_template, request
)
from .analysis import analysis
from analysis.models import analyse_sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from analysis.cache import get_recommended_stocks


analyzer = SentimentIntensityAnalyzer()
bp = Blueprint('index', __name__)

@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        ticker = request.form['ticker'].upper()
        return analysis(ticker)

    recommended_stocks = get_recommended_stocks()
    return render_template('index.html', recommended_stocks=recommended_stocks)


@bp.route('/contact', methods=["GET"])
def contact():
    return(render_template('contact.html'))


@bp.route('/about', methods=["GET"])
def about():
    return(render_template('about.html'))


@bp.route('/ai', methods=["GET", "POST"])
def ai():
    if request.method == 'POST':
        input = request.form['input']
        type = request.form['type']
        if type == 'financial-sentiment':
            sentiment, score = analyse_sentiment(input)
            return f"{{Sentiment: {sentiment.upper()}, Confidence score: {'{:.2f}'.format(abs(score))}}}"

        elif type == 'general-sentiment':
            score = analyzer.polarity_scores(input)['compound']
            return f"Polarity score: {score}"


    demo_text = "$MSFT No reason to not pick up this bargain for a bullish reversal"
    return(render_template('ai.html', demo_text=demo_text))
