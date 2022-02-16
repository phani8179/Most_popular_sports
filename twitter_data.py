import tweepy
import math
import datetime
from datetime import datetime

import pymongo
import requests

my_client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
my_data_base = my_client["test"]
my_collection = my_data_base["twitterdata"]

consumer_key="iFYKkZ1aUiKdF3oC1YltJQe0j"
consumer_secret="CFUErvTP8GMoABu0aM2SbbkKWtRIlSpoYrATXFcQFrY42JExaX"
access_token="2706455761-QvROLqGAVFwPb5CbQVgHF0WAD5IQvKXay1fDfMP"
access_token_secret="e4Lorr6dgIbva4DDlIj0nv4tHqjKMf1PnBthMJOqZmB9Z"

class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        data={}
        data['id']=status.id
        data['text']=status.text
        data['created']=status.created_at
        my_collection.insert_one(data)
        print(data)

# Initialize instance of the subclass
printer = IDPrinter(
  consumer_key, consumer_secret,
  access_token, access_token_secret
)

# Filter realtime Tweets by keyword
printer.filter(track=["sports","basketball","football","baseball","soccer","cricket","racing","F1","NBA","americanfootball"])
