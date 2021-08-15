# To The Moon
[![Jiaaa-yang](https://circleci.com/gh/Jiaaa-yang/orbital-to-the-moon.svg?style=shield)](https://app.circleci.com/pipelines/github/Jiaaa-yang/orbital-to-the-moon)

#### A web application that analyses the stock market sentiment

To The Moon is a project that utilises machine learning, where we collect our own data and train a _natural language processing_ model. We then use this model to process conversations about various stocks on social media, and provide investors an overview of the sentiment surrounding stocks they wish to invest in.

Check out our web application [here](https://orbital-to-the-moon.herokuapp.com/)

![Web homepage](../assets/images/web_app_homepage.png)

## About

This project is developed under [Orbital](https://orbital.comp.nus.edu.sg), an independent software engineering module by **NUS School of Computing**. Students are expected to work in pairs to develop a software of their choice, through self-learning from sources on the Internet. 

Project media:
* [Full documentation](https://drive.google.com/file/d/1c7jOcksoYp6OeN8eHZxcTnqx9DlGkuRF/view?usp=sharing)
* [Poster](https://drive.google.com/file/d/1k_UoCEXHOEKOckWaQ47U1MTuIUxlAiFQ/view?usp=sharing)
* [Video demonstration](https://drive.google.com/file/d/1zBYZ1tM0f8TNxXqOZ_F_K4mL9Um6BpXN/view?usp=sharing)

![Poster](../assets/images/poster.png?raw=true)


## Motivation
Ever wished that you were part of the **1000%** rally of GameStop’s stock? Or the **800%** rally of Signal Advance’s? Due to a Reddit coordinated short squeeze, and a two word tweet by Elon Musk respectively, prices of both stocks skyrocketed in a short period of time.

While such investments can be highly risky, these incidents have shown the impact social media can have on stock prices. We thus aim to collect information, mainly in the form of text, from social media to find a correlation between the text data collected and the change in stock prices.

Using _machine learning_, it is possible to classify this text data to understand the sentiments of other investors, and to use such analysis to predict short term price movements.

With the rise of young retail investors who increasingly exchange information on social media, we believe such analysis will become very valuable to understand the stock market.

## Main Features
1. **Stock analysis**
    * Analysis of a stock by searching for its ticker symbol
    * Includes prediction of its short term price movement, and also links to _tweets_ and news articles related to the stock

2. **Bullish stocks recommendation**
    * Provides a list of bullish stocks based on stocks other users have searched for

3. **Favourite stocks**
    * Adding stocks to a favourites list using session cookies
    * Allow users to access analysis of favourited stocks without typing its ticker symbol

4. **AI/About/Contact Us pages**
    * Static pages containing additional information for users, such as motivation of our project
    * Explanation of the _artificial intelligence_ used in our application, and for users to try out our sentiment classifier with custom input

## Machine Learning

The core of this project lies in our machine learning models, which performs the analysis on various stocks. The data used to train these models were mostly collected by us, using APIs from [Twitter](https://developer.twitter.com/en/docs/twitter-api) and [Alpha Vantage](https://www.alphavantage.co/). This is done by running our data collection script, `collect_data.py` on a daily basis. With this data, we have trained two machine learning models for our purpose.

Our first model is a **LinearSVC** model, which serves as our financial sentiment classifier. This model is in charge of predicting the sentiment of a tweet, based on its text content.

The second model is a **Random Forest Classifier**. This model is in charge of predicting whether the price of a stock will rise, based on the number of tweets of each sentiment as predicted by our first model.

Here, we provide links to Jupyter notebooks that were used in the development of our models, from data exploration to the final models used in our deployment.
1. [Twitter Data Exploration](https://www.kaggle.com/lyejiayang/1-twitter-data-exploration)
2. [Tweets classification](https://www.kaggle.com/lyejiayang/2-tweets-classification)
3. [Stock price prediction with tweets sentiment](https://www.kaggle.com/lyejiayang/3-stock-price-prediction-with-tweets-sentiment)
4. [Stock price prediction with finBert sentiment](https://www.kaggle.com/lyejiayang/4-stock-price-prediction-with-finbert-sentiment)

## Tech Stack
1. Python
2. HTML/CSS/Javascript
3. [Flask](https://flask.palletsprojects.com/en/2.0.x/)
4. [Twitter](https://developer.twitter.com/en/docs/twitter-api), [Alpha Vantage](https://www.alphavantage.co/), [Mediastack](https://mediastack.com/) APIs
5. [Scikit-learn](https://scikit-learn.org/stable/)
6. [MongoDB](https://www.mongodb.com/)
7. [SpaCy](https://spacy.io/)
 