from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
from typefight.db import get_db
import secrets

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/")
def auth():
    return render_template("auth.html")

@bp.route("/register", methods=["POST"])
def register():
    # when method is POST, user is sending the register form
    player_name = request.form["username"]
    password = request.form["password"]
    country = request.form["country"] if request.form["country"] != "" else None
    salt = secrets.token_hex(8)
    pass_salt = password + salt

    db = get_db()
    cur = db.cursor()
    error = None

    if not player_name:
        error = "Username is required."
    elif not password:
        error = "Password is required."
    else:
        cur.execute(
            "SELECT player_uid FROM players WHERE player_name = %s;", (player_name,)
        )
        # check if user already exists
        if cur.fetchone() is not None:
            error = f"Player name {player_name} already exists."
    
    # if all goes well, save user data into the database
    # and redirect user to main page
    if error is None:
        cur.execute(
            """
            INSERT INTO players(player_uid, player_name, country, salt, pass_hash) 
            VALUES(uuid_generate_v4(), %s, %s, %s, %s)
            """, (player_name, country, salt, generate_password_hash(pass_salt))
        )
        db.commit()
        return redirect(url_for("auth.auth"))

    cur.close()
    flash(error)
    return render_template("auth.html")
    
@bp.route("/login", methods=["POST"])
def login():
    player_name = request.form["username"]
    password = request.form["password"]

    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    error = None

    cur.execute(
        "SELECT * FROM players WHERE player_name = %s", (player_name,)
    )
    player = cur.fetchone()
    cur.close()

    if player is None:
        error = "Incorrect username."
    elif not check_password_hash(player["pass_hash"], password + player["salt"]):
        error = "Incorrect password."
    
    if error is None:
        session.clear()
        # if login was successful, store the user's id in a cookie for future requests
        #TODO CHANGE THIS TO A UNIQUE HASH INSTEAD OF player_uid
        session["player_uid"] = player["player_uid"]
        return redirect(url_for("game.index"))
    
    flash(error)
    return render_template("auth.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("game.index"))

@bp.before_app_request
def load_logged_in_user():
    player_uid = session.get("player_uid")

    if player_uid is None:
        g.user = None
    else:
        with get_db() as db:
            with db.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT player_name, country FROM players WHERE player_uid = %s", 
                    (player_uid, )
                    )
                g.user = cur.fetchone()
                cur.close()