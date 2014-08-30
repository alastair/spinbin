import twitter

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

twitterapi = twitter.Api(consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_key,
        access_token_secret=access_secret)

def send_update(name):
    msg = "New playlist for %s is now available. Get it at http://spinb.in" % name
    twitterapi.PostUpdate(msg)
