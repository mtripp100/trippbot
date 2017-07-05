from database import pick_phrase
import datetime
import tweepy
import os

def run():
    start = datetime.datetime.utcnow()
    print("Woke up at {}.".format(start))
    if not should_tweet(start):
        return

    phrase = pick_phrase()
    message = "\"{}\" — {}".format(phrase[0], phrase[1])
    print(message)

    api = get_api()
    status = api.update_status(status=message)
    print("Tweeted {}.".format(status.id_str))

def should_tweet(dt):
    rounded_hour = dt.time().hour if dt.time().minute < 30 else (dt.time().hour + 1) % 24
    ready = ((rounded_hour % 4) == 0)
    print("Nearest hour is {}, therefore tweet = {}.".format(rounded_hour, ready))
    return ready

def get_api():
    auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_SECRET'])

    return tweepy.API(auth)

if __name__ == "__main__":
    run()
