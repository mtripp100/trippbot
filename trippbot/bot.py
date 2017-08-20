from database import pick_phrase, record_phrase
import datetime
import os
import tweepy
import click
import requests

@click.command()
@click.option("--interval", default=4, help="The script is invoked once an hour, so only tweet "
              "if the current hour (UTC) divides exactly by this number.",
              type=click.IntRange(1, 24))
@click.option("--force", is_flag=True)
def run(interval, force):
    now = datetime.datetime.utcnow()
    if should_tweet(now, interval) or force:
        send_tweet()
    else:
        print("Nothing to do...")

    check_in()

def should_tweet(dt, interval):
    return ((dt.time().hour % interval) == 0)

def check_in():
    res = requests.get(os.environ["DEADMANSSNITCH_URL"])
    print(res.status_code, res.text)


MAX_TWEET_RETRIES = 5

def send_tweet():
    phrase = pick_phrase()
    url = build_url(phrase[0])
    message = "\"{}\" — {} {} #latin".format(phrase[1], phrase[2], url)
    print(message)

    api = get_api()
    for i in range(MAX_TWEET_RETRIES):
        try:
            status = api.update_status(status=message)
            record_phrase(status.id_str, phrase[0])
            break
        except tweepy.TweepError as t:
            print("#{}, error sending tweet: {}.".format(i, t))

def build_url(phrase_id):
    return "https://trippbot.herokuapp.com/q/{}".format(phrase_id)

def get_api():
    auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_SECRET"])

    return tweepy.API(auth)


if __name__ == "__main__":
    run()
