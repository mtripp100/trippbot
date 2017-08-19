import os
import psycopg2.extras
import urllib.parse
import contextlib

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

@contextlib.contextmanager
def _get_cursor(connection):
    with connection as conn:
        with conn.cursor() as cursor:
            yield cursor


_connection = _get_connection()

def upload_phrases(phrases):
    with _get_cursor(_connection) as cursor:
        psycopg2.extras.execute_values(
            cursor,
            "INSERT INTO phrases(latin, translation, notes) VALUES %s "
            "ON CONFLICT(latin) DO UPDATE "
            "SET translation=excluded.translation, notes=excluded.notes",
            phrases
        )

def pick_phrase():
    with _get_cursor(_connection) as cursor:
        cursor.execute(
            "SELECT phrase_id, latin, translation, notes "
            "FROM phrases ORDER BY RANDOM() LIMIT 1"
        )
        return cursor.fetchone()

def record_phrase(tweet_id, phrase_id):
    with _get_cursor(_connection) as cursor:
        cursor.execute(
            "INSERT INTO tweets(tweet_id, phrase_id) "
            "VALUES (%s, %s)", (tweet_id, phrase_id)
        )

def get_phrase(phrase_id):
    with _get_cursor(_connection) as cursor:
        try:
            cursor.execute(
                "SELECT latin, translation, notes "
                "FROM phrases WHERE phrase_id=%(phrase_id)s",
                {"phrase_id": phrase_id}
            )
        except psycopg2.DataError:
            return None
        return cursor.fetchone()
