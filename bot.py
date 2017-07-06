from database import pick_phrase, record_phrase
import tweepy
import os

def run():
    phrase = pick_phrase()
    message = "\"{}\" — {}".format(phrase[1], phrase[2])
    print(message)

    api = get_api()
    status = api.update_status(status=message)

    record_phrase(status.id_str, phrase[0])

def get_api():
    auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_SECRET'])

    return tweepy.API(auth)

if __name__ == "__main__":
    run()
