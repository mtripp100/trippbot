from database import pick_phrase, record_phrase
from datetime import datetime
import os
import tweepy
import click

@click.command()
@click.option("--interval", default=4, help="The script is invoked once an hour, so only tweet "
              "if the current hour (UTC) divides exactly by this number.",
              type=click.IntRange(1, 24))
@click.option("--force", is_flag=True)
def run(interval, force):
    if force:
        send_tweet()
        return

    now = datetime.utcnow()
    if should_tweet(now, interval):
        send_tweet()
        return

    print("Nothing to do...")

def send_tweet():
    phrase = pick_phrase()
    url = build_url(phrase[0])
    message = "\"{}\" — {} {} #latin".format(phrase[1], phrase[2], url)
    print(message)

    api = get_api()
    status = api.update_status(status=message)

    record_phrase(status.id_str, phrase[0])

def get_api():
    auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_SECRET'])

    return tweepy.API(auth)

def should_tweet(dt, interval):
    return ((dt.time().hour % interval) == 0)

def build_url(phrase_id):
    return "https://trippbot.herokuapp.com/q/{}".format(phrase_id)


if __name__ == "__main__":
    run()
