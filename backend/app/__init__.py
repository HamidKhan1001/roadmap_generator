from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.db import init_db
from app.routes import api


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["CORS_ORIGINS"]
            }
        },
    )

    with app.app_context():
        init_db()

    app.register_blueprint(api, url_prefix="/api")

    return app