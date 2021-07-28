from flask import current_app, g
import psycopg2

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            user=current_app.config["DB_USER"],
            database=current_app.config["DB_NAME"],
            password=current_app.config["DB_PASSWORD"],
            host=current_app.config["DB_HOST"]
        )
    return g.db

def close_db(exception=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()