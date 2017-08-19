from flask import render_template, abort
from web import app
import database

@app.route("/q/<quote_id>")
def quote(quote_id):
    quote = database.get_phrase(quote_id)
    if not quote:
        return abort(404)
    return render_template("quote.html", quote=quote)
