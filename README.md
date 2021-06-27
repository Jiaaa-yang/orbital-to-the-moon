# To The Moon
#### Proposed Level of Achievement: Apollo 11
#### An AI web application that analyses the stock market sentiment
To The Moon aims to use _natural language processing_ to process large amounts of social media posts on different stocks. By analysing these conversations over the internet, we provide users with the general sentiment surrounding the stocks that they wish to invest in.

[Website](https://orbital-to-the-moon.herokuapp.com) (For people not experienced with stocks, try entering popular symbols like 'TSLA' or 'AMC')
![Web homepage](../assets/images/web_app_homepage.png?raw=true)

## Motivation
Ever wished that you were part of the **1000%** rally of GameStop’s stock? Or the **800%** rally of Signal Advance’s? Due to a **Reddit** coordinated short squeeze, and a two word tweet by Elon Musk respectively, prices of both stocks skyrocketed in a short period of time.

While such investments can be highly risky, these incidents have shown the impact social media can have on stock prices. We thus aim to collect such information, mainly in the form of text, from social media to find a correlation between such information and change in stock prices.

Using _artificial intelligence_, it is possible to classify this text data to understand the sentiments of other investors, and to use such analysis to predict short term price movements.

With the rise of young retail investors who increasingly exchange information on social media, we believe such analysis will become very valuable to understand the market.

## User Stories
>*"I am a retail investor and I have done my due diligence for a company I want to invest in. However the stock prices seem to be falling and I am not sure if I want to buy in now. I want to know if the stock prices will continue to fall."*

>*"I am a retail investor and the stock that I am holding is falling. I am not aware of any news related to it. I want to know what other investors are thinking about this stock."*

>*"I am an investor with a long investment horizon holding several stocks. I am not interested in short term price changes, and I do not spend much time on every single news about my stocks. I would like a quick summary to just know the sentiment of recent news articles on my stocks."*

>*"I am an investor looking to buy into a stock. I usually look at some chatters on the stock I am interested in before buying, but it can be hard to filter out the relevant ones. I would like to see some top tweets in terms of bullish/bearish sentiments."*

## Overview
![Project Overview](../assets/images/project_overview.png?raw=true)
## Core Features

### Frontend:
A web application that allows users to
+ Search for a stock and get the analysis for the sentiment of the stock based on **Twitter** data 
+ Get a prediction of whether chosen stock is likely to _rise_ or _fall_ in the short term
+ Get an overview of recent news of about the chosen stock and their general sentiment

![User flow diagram](../assets/images/user_flow_diagram.png?raw=true)


### Backend:
+ Data collection scripts to save _tweets_ and _prices data_ for training of AI
+ **Machine learning model** that can predict direction of price movement by analysing recent _tweets_ about a stock

### Possible Extensions:
+ View a list of stocks with the most bullish sentiment
+ Put stocks on watchlist to track daily changes in sentiment

## Data collection
In order to train a machine learning model, we will require a large amount of relevant data. In this case, we need _financial tweets_ and _prices data_ about various stocks traded. We thus chose a set of **300** most actively traded stocks and used APIs from **Twitter** and **Alpha Vantage** to get the relevant data. We developed a script that can be run regularly to get these data and save them, and allowed us to collect sufficient data for training of machine learning models.
![Data collection phase](../assets/images/data_collection.png?raw=true)

## Artificial Intelligence
For the AI portion of the project, we have developed 2 _machine learning_ models. The first is a **LinearSVC** model that classifies the financial sentiment of the text of a tweet. To pass our text data into the model, we used a bag of words model by transforming our corpus into a **TF-IDF matrix**. This model allows us to predict the financial sentiment of each tweet with regards to the stock it is referring to.

The second model is a **Random Forest Classifier** which predicts whether the price of a stock will rise or fall, based on the tweets associated with the stock. This model uses the first model to label each tweet associated with a particular stock. Then, using the number of positive/bullish tweets on the stock, the model predicts whether this stock will rise or fall.

As of the time of writing, both models have an accuracy of about **61%** for their binary classification task. While this accuracy is not ideal, the nature of the task, which is to predict stock prices using social media sentiments, is not exactly straightforward. The accuracy will be worked on as more data is collected.

For the full process of training the two models, and also the exploration of the tweets data collected, check out these notebooks:
* [Tweets EDA](https://www.kaggle.com/lyejiayang/1-twitter-data-exploration)
* [Tweets sentiment classification](https://www.kaggle.com/lyejiayang/2-tweets-classification)
* [Stock price prediction](https://www.kaggle.com/lyejiayang/3-stock-price-prediction-with-tweets-sentiment)

## Development Timeline

### May
+ Design of static web user interface
+ Mining of **Twitter** data for various popular stock tickers
+ Research on common NLP techniques for **text classification** and **sentiment analysis**

### June
+ Perform **Exploratory Data Analysis** on collected data to visualise the collected data
+ _Training_ and _tuning_ of machine learning models using collected data
+ **Integration** of trained models with web application
+ _User_ and _system_ testing to discover bugs

### July
+ Further improvement on **accuracy** of machine learning models
+ Fixing of bugs based on collected feedback
+ Extension of frontend features of web application

## Testing and Logging
#### Testing
For testing, we are currently using Python's built-in [unittest](https://docs.python.org/3/library/unittest.html) module. Our approach is currently to write tests for every minor functionality in our program. This includes testing for the return type of each function, and the expected range of values, like the probability score returned by our models. 

This ensures that subsequent code that builds on smaller functions does not have to worry about the correctness of those functions. This gives us the assurance that changes to the code in the future will not break our program.

Since we also work with multiple APIs, we also ensure that the APIs return values in forms we expect. This ensures that we can adapt to changes by the APIs if necessary.

###### Issues found and fixes:
* Alpha Vantage API returns date in the form of 'YYYY-MM-DD', which was inconsistent with our date format in other parts of the program. We have ensured that all our date formats are consistent in the form of 'YYYY-MM-DD'.
* When refactoring our code to encapsulate data returned by APIs as custom classes rather than key-value pairs, a function that uses the APIs expecting a key-value form failed the test. The function was fixed to accept the custom class instead.

#### Logging
Additionally, we are also using logs to keep track of our data collection process. Since the process is automated, keeping a data collection log allows us to keep track of our data collection process with minimal effort. The log contains information such as the type of data, and the last timestamp of data collection. We also log errors that result in data not being written fully, such as exceptions due to API rate limits.

## Tech Stack
1. Python
2. HTML/CSS/Javascript
3. [Flask](https://flask.palletsprojects.com/en/2.0.x/)
4. [Twitter](https://developer.twitter.com/en/docs), [Alpha Vantage](https://www.alphavantage.co/) APIs
5. Machine Learning libraries: Sklearn, Tensorflow
6. Natural Language libraries: NLTK, SpaCy
