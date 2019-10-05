from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Construct the core application."""

    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    with flask_app.app_context():
        from . import docs
        from . import routes

        return flask_app
