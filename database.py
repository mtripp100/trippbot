from ingest import ingest_compact
import psycopg2
import psycopg2.extras
import os
import urllib.parse

def get_connection():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

def do_upload():
    phrases = ingest_compact()
    conn = get_connection()

    with conn.cursor() as cursor:
        psycopg2.extras.execute_values(cursor, "INSERT INTO phrases(latin, translation, notes) VALUES %s", phrases)
        conn.commit()

do_upload()
