from flask import render_template, Blueprint, jsonify
from psycopg2.extras import RealDictCursor

from typefight.db import get_db
from typefight.utils import make_serializable

bp = Blueprint("game", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/highscores")
def get_highscores():
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT scores.score, players.player_name, players.country FROM scores
        LEFT JOIN players
        ON players.player_uid = scores.player_uid;
        """
    )

    scores_table = cur.fetchall()
    cur.close()

    return jsonify(make_serializable(scores_table))

@bp.route("/quote")
def get_quote():
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT quote FROM quotes ORDER BY RANDOM() LIMIT 1;
        """
    )

    quote = cur.fetchone()
    cur.close()

    return jsonify(quote)