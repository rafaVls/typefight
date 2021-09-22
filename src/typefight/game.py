from flask import (
    render_template, Blueprint, jsonify, request, g, session
)
from psycopg2.extras import RealDictCursor

from typefight.db import get_db
from typefight.utils import make_serializable
from typefight.auth import login_required

import contextlib

bp = Blueprint("game", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/highscores")
def get_highscores():
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)

    quote_id = g.quote_id
    scores_table = []

    try:
        cur.execute(
            """
            SELECT scores.score, players.player_name, players.country
            FROM scores
            LEFT JOIN players
            ON players.player_uid = scores.player_uid
            WHERE scores.quote_uid = %s;
            """, (quote_id, )
        )
        scores_table = cur.fetchall()

    except Exception as e:
        print(f"An exception has occured during {request}:", e)
        print("Exception TYPE: ", type(e))

    cur.close()

    return jsonify(make_serializable(scores_table))

@bp.route("/highscores/<float:score>", methods=["POST"])
@login_required
def set_highscore(score):
    #TODO make sure "score" doesn't contain slash (/)
    db = get_db()

    server_response = {
        "success": False,
        "message": None
    }

    player_name = g.user["player_name"]
    quote_id = g.quote_id
    existing_score = None

    with contextlib.closing(db.cursor(cursor_factory=RealDictCursor)) as cur:
        cur.execute(
            """
            SELECT player_uid
            FROM players
            WHERE player_name = %s;
            """, (player_name, )
        )
        player_uid = cur.fetchone()["player_uid"]

        try:
            cur.execute(
                """
                SELECT players.player_uid, scores.score
                FROM scores
                LEFT JOIN players
                ON players.player_uid = scores.player_uid
                WHERE player_name = %s
                AND quote_uid = %s;
                """, (player_name, quote_id)
            )
            existing_score = cur.fetchone()
        
        except Exception as e:
            server_response["message"] = e
            print(f"An exception has occured during {request}:", e)
            print("Exception TYPE:", type(e))

        if existing_score is None:
            cur.execute(
                """
                INSERT INTO scores(player_uid, quote_uid, score)
                VALUES (%s, %s, %s);
                """, (player_uid, quote_id, score)
            )
            db.commit()

            server_response["success"] = True
            server_response["message"] = f"Your new score {score} has been saved."
            
        elif score < existing_score["score"]:
            cur.execute(
                """
                UPDATE scores
                SET score = %s
                WHERE player_uid = %s
                AND quote_uid = %s;
                """, (score, player_uid, quote_id)
            )
            db.commit()

            server_response["success"] = True
            server_response["message"] = f"New record! Your new score was faster than your previous one. Old score: {existing_score['score']} New score: {score}"
        else:
            server_response["success"] = True
            server_response["message"] = f"Too slow! Best score: {existing_score['score']} Current score: {score}"

    return server_response

@bp.route("/quote")
def get_quote():
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT quote, quote_uid AS quote_id 
        FROM quotes 
        ORDER BY RANDOM() 
        LIMIT 1;
        """
    )
    quote = cur.fetchone()
    session["quote"] = quote
    cur.close()

    return jsonify(quote)

@bp.before_app_request
def load_current_quote():
    quote = session.get("quote")

    if quote is None:
        g.quote_id = None
    else:
        g.quote_id = quote["quote_id"]
