from trippbot.database import get_phrase
from flask import Flask, render_template, abort

app = Flask(__name__)

@app.route("/q/<quote_id>")
def quote(quote_id):
    quote = get_phrase(quote_id)
    if not quote:
        return abort(404)
    return render_template("quote.html", quote=quote)
