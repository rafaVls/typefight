import os

from flask import Flask
from . import auth, db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")

    app.config["SECRET_KEY"] = SECRET_KEY

    app.register_blueprint(auth.bp)
    
    # this tells flask to call close_db on cleanup
    app.teardown_appcontext(db.close_db)
    return app