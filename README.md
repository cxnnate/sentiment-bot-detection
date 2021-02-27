# Sentiment Bot Detector

This projects stems from a problem I was trying to solve at my job. I never got to finish it, but I wanted to keep working on it. The goal of the project was to perform analysis on tweets. We wanted to understand how social spambots affect the overall sentiment of a topic. My aim for this project is to turn this idea into a usable web application and expand the services by implementing state-of-the-art natural language processing techiques to fight disinformation. 

## Data Collecting

Data is collected from Twitter using Tweepy. 

To start the data streaming tool, ensure Tweepy is installed

`pip install tweepy` then run,
`python3 stream.py --creds <credentials> --keys <keywords> --time 5`

Arguments
- creds: A JSON file of Twitter API credentials. Apply for one here
- keys: A file of keywords to filter the stream
- time: Time limit

## Topic Model

Search for latent topics in the data

## Sentiment Analysis

Classify the polarity of a given tweet

## Bot Detection

Produce a bot score based on the given features


### Author
Nate