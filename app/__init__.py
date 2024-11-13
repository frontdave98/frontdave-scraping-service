from flask import Flask
from app.routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Register Blueprints
    app.register_blueprint(api)

    return app