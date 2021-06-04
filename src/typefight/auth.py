from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from typefight.db import get_db, close_db
import secrets

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    # when method is POST, user is sending the register form
    if request.method == "POST":
        player_name = request.form["player_name"]
        password = request.form["password"]
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
                INSERT INTO players(player_uid, player_name, salt, pass_hash) 
                VALUES(uuid_generate_v4(), %s, %s, %s)
                """, (player_name, salt, generate_password_hash(pass_salt))
            )
            db.commit()
            return redirect(url_for("game.index"))

        flash(error)
        cur.close()
        close_db()
    
    return render_template("auth/register.html")