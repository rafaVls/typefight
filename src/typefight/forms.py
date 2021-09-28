from wtforms import (
    Form, StringField, PasswordField, SelectField, validators, ValidationError
)

from werkzeug.security import check_password_hash
from psycopg2.extras import RealDictCursor

from typefight.utils import get_countries_list, get_countries_path 
from typefight.db import get_db

import contextlib

# ==========[ REGISTRATION FORM ]========== #
countries = get_countries_list(get_countries_path())
for i in range(0, len(countries)):
    countries[i] = (countries[i], countries[i])
countries.insert(0, ("", "Select a country..."))

def existing_player_check(_, field):
    db = get_db()

    with contextlib.closing(db.cursor()) as cur:
        cur.execute(
            """
            SELECT player_uid
            FROM players
            WHERE player_name = %s;
            """, (field.data, )
        )

        if cur.fetchone() is not None:
            raise ValidationError(f'Player name "{field.data}" already exists')

class RegistrationForm(Form):
    username = StringField(
        "Username", 
        [
        validators.DataRequired(message="A username is required"),
        validators.Length(max=15, message="Keep the username below 15 characters"),
        validators.Regexp(r"^\w+$", message='Only letters, numbers, and underscores'),
        existing_player_check
        ],
        render_kw={"placeholder": "el_Camino23"}
    )

    password = PasswordField(
        "Password", 
        [
        validators.DataRequired(message="A password is required"),
        validators.Length(min=6, message="Password must be at least 6 characters long"),
        validators.EqualTo("confirm", message="Passwords don't match")
        ],
        render_kw={"placeholder": "safePassword123"}
    )

    confirm = PasswordField(
        "Confirm Password", 
        render_kw={"placeholder": "safePassword123"}
    )

    country = SelectField("Country", choices=countries)


# ==========[ LOGIN FORM ]========== #
def database_check(form, field):
    db = get_db()

    with contextlib.closing(db.cursor(cursor_factory=RealDictCursor)) as cur:
        cur.execute(
            """
            SELECT *
            FROM players
            WHERE player_name = %s
            """, (form.username.data, )
        )
        player = cur.fetchone()

    if player is None:
        if field.id == "username":
        # this is to show the error message under the correct input
            raise ValidationError(f'Username "{field.data}" not found')
    else:
        if field.id == "password":
            if not check_password_hash(player["pass_hash"], field.data + player["salt"]):
                raise ValidationError("Incorrect password")

class LoginForm(Form):
    username = StringField(
        "Username", 
        [
        validators.DataRequired(message="A username is required"),
        validators.Length(max=15, message="Usernames are below 15 characters"),
        database_check
        ],
        render_kw={"placeholder": "registered_Player23"}
    )

    password = PasswordField(
        "Password", 
        [
        validators.DataRequired(message="A password is required"),
        database_check
        ],
        render_kw={"placeholder": "safePassword123"}
    )
