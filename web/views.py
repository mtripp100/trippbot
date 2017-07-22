from flask import render_template, abort
from web import app

import database
import psycopg2

@app.route('/q/<quote_id>')
def quote(quote_id):
    try:
        quote = database.get_phrase(quote_id)
        return render_template('quote.html', quote=quote)
    except psycopg2.DataError:
        return abort(400)

