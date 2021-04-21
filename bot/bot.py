"""
This file was created by Mayur Bhoi (mayur57) at 18:31 on 19-April-2021
and is covered under MIT License for free use. The project is open source.
For more information on licensing, visit https://opensource.org/licenses/MIT
and to read the license clauses refer to the included LICENSE file.
"""

import tweepy
import time
from datetime import date

# Declaring API keys and Consumer Keys
# Generate your keys and replace with below placeholders
consumer_key = '<YOUR-KEY-HERE>'
consumer_secret = '<YOUR-KEY-HERE>'
access_token = '<YOUR-KEY-HERE>'
access_token_secret = '<YOUR-KEY-HERE>'

# Take the keys and authenticate the bot
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Establish an API object for using the methods
# Since the scale of tweets in this case is huge,
# the API should not stop when the rate limits are reached.
# Therefore, => wait_on_rate_limit is set to True
api = tweepy.API(auth, wait_on_rate_limit=True) 


# The bot searches for tweets with following hashtags
hashtags = [
    "#Remdesvir",
    "#remdesivir",
    "#COVIDResourceBot", #hashtag for enabling already existing tweet threads
    "#oxygen"
    ]

# The bot will only look for tweets published on the present day
# 25 tweets at a time to avoid reaching rate limits
date_since = date.today()
tweet_count = 25

# Define a delay between each retweet to avoid processing overloading
RETWEET_DELAY = 5 #seconds

# Define the delay between each polling round to avoid
POLLING_DELAY = 300 #seconds

# Retweet given a tweet's ID
def retweet(id):
    try:
        print("---Retweeting: " + str(id))
        api.retweet(id)
        time.sleep(RETWEET_DELAY)

    except Exception as e:
        print("ERROR: ---" + e.reason)

# Handle the #covidresourcebot special hashtag
def retweet_parent(tweet):

    # If tweet has a parent tweet, retweet parent
    if tweet.in_reply_to_status_id != "None":
        # try-catch avoid the bot from exiting the program
        try:
            print("!!!- RT hashtag was detected. Retweeting parent: " + str(tweet.in_reply_to_status_id))
            api.retweet(tweet.in_reply_to_status_id)
            time.sleep(RETWEET_DELAY)
        except Exception as e:
            print("ERROR: ---" + e.reason)

    # else retweet the tweet itself
    else:
        retweet(tweet.in_reply_to_status_id)

# Define a search function that fetches and processes the tweets
def searchBot():
    for hashtag in hashtags:
        tweets = tweepy.Cursor(api.search, hashtag, since=date_since).items(tweet_count)
        for tweet in tweets:
            if "#covidresourcebot" in tweet.text:
                retweet_parent(tweet)
            else:
                retweet(tweet.id)

# Infinitely run the function with a polling delay
while(True):
    searchBot()
    time.sleep(POLLING_DELAY)