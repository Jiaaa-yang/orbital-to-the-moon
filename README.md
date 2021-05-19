# To The Moon

Were you hoping that you had bought GameStop’s stocks before it rocketed? Or sold your holdings when it started plunging? While meme stocks are dangerous and not the way to go for general investors in the market, this incident has shown a great impact social media can have on stocks, whose prices are driven by demand.

Wouldn't it be great if we could analyze the sentiments of a stock you wanted to buy, after doing the required due diligence of course, before deciding to buy it? Seeing how Elon Musk’s tweets can drive prices of stock up effortlessly, Twitter alone could contain huge amounts of information for people. 

We want to leverage on this huge amount of information by applying data mining techniques and natural language processing to perform sentiment analysis on Twitter posts and predict stocks prices.


## User Stories
>*"I am a retail investor and I have done my due diligence for a company I want to invest in. However the stock prices seem to be falling and I am not sure if I want to buy in now. Can I know what other investors are saying about this stock?"*

>*"My portfolio consists of over 10 stocks, and I don’t have the time to go through all the news. I would really like to get a quick summary on the stocks to see if news articles are bullish or bearish on my stocks"*


## Core Features
The web application allows users to
+ Get up-to-date price predictions for popular stocks based on Twitter and Reddit data
+ Get an overview of recent news of stocks and whether the general sentiment is positive or negative

### Possible Extensions:
+ View a list of top picks


## Development Timeline

### May
+ Design of static web user interface
+ Mining of **Twitter** and **Reddit** text data based on various stock tickers
+ Research on common NLP techniques for **text classification** and **sentiment analysis**

### June
+ _Training_ and _tuning_ of machine learning models using mined data
+ **Integration** of backend models with web interface

### July
+ _User_ and _system_ testing to discover bugs
+ **Extension** of features based on collected feedback

## Tech Stack
1. Python-Flask framework
2. HTML/CSS/Javascript
3. Twitter, Reddit APIs
4. Machine Learning libraries: Sklearn, Tensorflow
5. Natural Language libraries: NLTK, SpaCy
