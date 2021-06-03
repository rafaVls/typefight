import os

from flask import g
import psycopg2

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            user=os.environ["DB_USER"],
            database=os.environ["DB_NAME"],
            password=os.environ["DB_PASSWORD"],
            host="database"
        )
    return g.db

def close_db():
    db = g.pop("db", None)

    if db is not None:
        db.close()