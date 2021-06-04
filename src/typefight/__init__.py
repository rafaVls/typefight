from flask import Flask
from . import auth

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    @app.route("/hello")
    def hello():
        return "Hello, world!"

    app.register_blueprint(auth.bp)
    
    return app