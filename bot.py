from database import pick_phrase, record_phrase
import datetime
import tweepy
import os

def run():
#     start = datetime.datetime.utcnow()
#     print("Woke up at {}.".format(start))
#     if not should_tweet(start):
#         return

    phrase = pick_phrase()
    message = "\"{}\" — {}".format(phrase[1], phrase[2])
    print(message)

    api = get_api()
    status = api.update_status(status=message)

    record_phrase(status.id_str, phrase[0])

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
