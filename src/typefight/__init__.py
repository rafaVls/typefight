import os

from flask import Flask, render_template
from . import auth, db, game

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")

    app.config["SECRET_KEY"] = SECRET_KEY

    app.register_blueprint(auth.bp)
    app.register_blueprint(game.bp)
    
    # this tells flask to call close_db on cleanup
    app.teardown_appcontext(db.close_db)

    # move this to "game" blueprint in the future
    @app.route("/")
    def home():
        return render_template("index.html")

    return app