import os
import random
import tweepy
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
        "oh dear.",
        "big bother.",
        "oh man.",
        "crime car alert!",
        "look at this dirty criminal.",
        "keep your eyes peeled!",
        "news just in.",
        "another one?",
        "terrible. Simply terrible.",
        "I'm distraught.",
        "what an absolute travesty.",
        "get the plod on this.",
    ])


def tweet(twt, dvla, plate, police_twt):
    starter = random_starter()
    colour = dvla["colour"]
    year = str(dvla["yearOfManufacture"])
    make = dvla["make"]

    tweet_text = \
        '@' + police_twt + ' ' + starter + \
        " This " + colour.lower() + ' ' + year + ' ' + make + \
        " with registration " + plate

    tax = is_taxed(dvla)
    mot = has_MOT(dvla)

    # Tax but no MOT
    if tax and not mot:
        tweet_text += " has no valid MOT!"
    # No tax but MOT
    elif not tax and mot:
        tweet_text += " has no valid road tax!"
    # No tax or MOT
    elif not tax and not mot:
        tweet_text += " has no road tax or valid MOT!"
    # Tax and MOT
    else:
        return

    twt.create_tweet(text=tweet_text)
