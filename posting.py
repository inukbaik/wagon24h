import tweepy
import os
from dotenv import load_dotenv


def initialize_tweepy_api():
    load_dotenv()
    api = tweepy.Client(
        bearer_token=os.getenv('BEARER_TKN'),
        access_token=os.getenv('ACCESS_TKN'),
        access_token_secret=os.getenv('ACCESS_SECRET'),
        consumer_key=os.getenv('API_KEY'),
        consumer_secret=os.getenv('API_SECRET')
    )
    return api


def post_tweet(api, tweet_text, media_ids):
    api.create_tweet(text=tweet_text, media_ids=media_ids)
    print("Posted Successfully")