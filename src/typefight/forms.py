from wtforms import (
    Form, StringField, PasswordField, SelectField, validators, ValidationError
)

from typefight.utils import get_countries_list, get_countries_path 
from typefight.db import get_db
import contextlib

countries = get_countries_list(get_countries_path())
for i in range(0, len(countries)):
    countries[i] = (countries[i], countries[i])
countries.insert(0, ("", "Select a country..."))

def existing_player_check(form, field):
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
            raise ValidationError(f"Player name {field.data} already exists")

class RegistrationForm(Form):
    username = StringField("Username", [
        validators.DataRequired(message="A username is required"),
        validators.Length(max=15, message="Keep the username below 15 characters"),
        existing_player_check
    ])
    password = PasswordField("Password", [
        validators.DataRequired(message="A password is required"),
        validators.EqualTo("confirm", message="Passwords don't match")
    ])
    confirm = PasswordField("Confirm Password")
    country = SelectField("Country", choices=countries)

