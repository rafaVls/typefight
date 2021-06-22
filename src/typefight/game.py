from flask import Blueprint, jsonify
from psycopg2.extras import RealDictCursor

from typefight.db import get_db
from typefight.utils import make_serializable

bp = Blueprint("game", __name__, url_prefix="/game")

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