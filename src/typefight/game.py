import json
from flask import Blueprint
from psycopg2.extras import RealDictCursor

from typefight.db import get_db
from . import utils

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

    scores = json.dumps(scores_table, default=utils.decimal_type_handler)
    return scores