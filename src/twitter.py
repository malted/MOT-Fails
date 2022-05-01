import tweepy
import os
import random
from dvla import is_taxed, has_MOT

def twitter_client():
    return tweepy.Client(
        bearer_token=os.environ["TWITTER_BEARER"],
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_KEY_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )

def random_starter():
    return random.choice([
        "SMH.",
        "Oh dear.",
        "Big bother.",
        "Oh man.",
        "Crime car alert!",
        "Look at this dirty criminal.",
        "Keep your eyes peeled!",
        "News just in.",
        "Another one?",
        "Terrible. Simply terrible.",
        "I'm distraught."
        "What an absolute travesty.",
        "Someone call the plod!",
    ])


def tweet(twt, dvla, plate):
    starter = random_starter()
    colour = dvla["colour"]
    year = dvla["yearOfManufacture"]
    make = dvla["make"]

    tweet_text = \
        starter + " This " + colour + ' ' + year + ' ' + make + ' ' + plate

    tax = is_taxed(dvla)
    mot = has_MOT(dvla)

    # Tax and MOT
    if tax and mot:
        return
    # Tax but no MOT
    elif tax and not mot:
        tweet_text += " has no valid MOT!"
    # No tax but MOT
    elif not tax and mot:
        tweet_text += " has no valid road tax!"
    # No tax or MOT
    elif not tax and not mot:
        tweet_text += " has no road tax or valid MOT!"
        
    twt.create_tweet(text=tweet_text)