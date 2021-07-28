from flask import Flask
from . import auth, db, game

def create_app(config_filename="flask.cfg"):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile(config_filename)
    app.register_blueprint(auth.bp)
    app.register_blueprint(game.bp)
    
    # this tells flask to call close_db on cleanup
    app.teardown_appcontext(db.close_db)

    return app