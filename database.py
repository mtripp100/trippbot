import psycopg2
import psycopg2.extras
import os
import urllib.parse

def _get_connection():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

_connection = _get_connection()

def do_upload(phrases):
    with _connection.cursor() as cursor:
        psycopg2.extras.execute_values(cursor, "INSERT INTO phrases(latin, translation, notes) VALUES %s", phrases)
        _connection.commit()

def pick_phrase():
    with _connection.cursor() as cursor:
        cursor.execute("SELECT phrase_id, latin, translation, notes FROM phrases ORDER BY RANDOM() LIMIT 1")
        _connection.commit()
        return cursor.fetchone()

def record_phrase(tweet_id, phrase_id):
    with _connection.cursor() as cursor:
        cursor.execute("INSERT INTO tweets(tweet_id, phrase_id) VALUES (%s, %s)", (tweet_id, phrase_id))
        _connection.commit()
