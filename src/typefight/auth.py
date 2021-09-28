from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import generate_password_hash
from psycopg2.extras import RealDictCursor

from typefight.db import get_db
import typefight.forms as forms
from datetime import datetime

import contextlib
import functools
import secrets
import hashlib

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegistrationForm(request.form)
    
    if request.method == "POST" and form.validate():
        player_name = form.username.data
        password = form.password.data
        country = form.country.data
        salt = secrets.token_hex(8)
        pass_salt = password + salt

        db = get_db()
        with contextlib.closing(db.cursor()) as cur:
            cur.execute(
                """
                INSERT INTO players(player_uid, player_name, country, salt, pass_hash) 
                VALUES(uuid_generate_v4(), %s, %s, %s, %s);
                """, (player_name, country, salt, generate_password_hash(pass_salt))
            )
            db.commit()

        return redirect(url_for(".login"))

    return render_template(
        "auth.html", 
        register_form=form,
        login_form=forms.LoginForm()
    )
    
@bp.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm(request.form)

    if request.method == "POST" and form.validate():
        player_name = form.username.data

        db = get_db()
        with contextlib.closing(db.cursor(cursor_factory=RealDictCursor)) as cur:
            cur.execute(
                """
                SELECT * 
                FROM players 
                WHERE player_name = %s;
                """, (player_name, )
            )
            player = cur.fetchone()

        # if login was successful, store the session hash in session for future requests
        session.clear()
        now = datetime.now().strftime("%H%M%S")
        encoded_str = str(player["player_name"] + now).encode("utf-8")
        session_hash = hashlib.sha512(encoded_str).hexdigest()

        with contextlib.closing(db.cursor()) as cur:
            try:
                cur.execute(
                    """
                    SELECT session_hash
                    FROM sessions
                    WHERE player_uid = %s;
                    """, (player["player_uid"], )
                )
                existing_session = cur.fetchone()

                if existing_session is None:
                    cur.execute(
                        """
                        INSERT INTO sessions(session_hash, player_uid)
                        VALUES(%s, %s);
                        """, (session_hash, player["player_uid"])
                    )
                    db.commit()
                else:
                    cur.execute(
                        """
                        UPDATE sessions
                        SET session_hash = %s,
                            login_date = NOW()
                        WHERE player_uid = %s;
                        """, (session_hash, player["player_uid"])
                    )
                    db.commit()

            except Exception as e:
                print(f"An exception has occured during {request}:", e)
                print("Exception TYPE: ", type(e))

        session["session_hash"] = session_hash
        return redirect(url_for("game.index"))
    
    return render_template(
        "auth.html", 
        register_form=forms.RegistrationForm(), 
        login_form=form,
        login=True
    )

@bp.route("/logout")
def logout():
    session_hash = session.get("session_hash")
    session.clear()

    with get_db() as db:
        with contextlib.closing(db.cursor()) as cur:
            cur.execute(
                """
                DELETE FROM sessions
                WHERE session_hash = %s;
                """, (session_hash, )
            )
            db.commit()

    return redirect(url_for("game.index"))

@bp.before_app_request
def load_logged_in_user():
    session_hash = session.get("session_hash")

    if session_hash is None:
        g.user = None
    else:
        with get_db() as db:
            with contextlib.closing(db.cursor(cursor_factory=RealDictCursor)) as cur:
                cur.execute(
                    """
                    SELECT player_uid
                    FROM sessions
                    WHERE session_hash = %s;
                    """, (session_hash, )
                )
                player_uid = cur.fetchone()["player_uid"]

                cur.execute(
                    """
                    SELECT player_name, country 
                    FROM players 
                    WHERE player_uid = %s;
                    """, (player_uid, )
                    )
                g.user = cur.fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):

        if g.user is not None:
           return view(**kwargs)
        else:
            #TODO redirect to a login page or something
            return "You need to be logged in to access this content"

    return wrapped_view
