from flask import Flask
from flask_jwt_extended.jwt_manager import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()


def create_app():
    """
        Construct the core application.
    """

    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    login_manager.init_app(flask_app)
    jwt.init_app(flask_app)

    with flask_app.app_context():
        from . import admin
        from . import commands
        from . import docs
        from . import routes
        from . import schemes

        return flask_app
