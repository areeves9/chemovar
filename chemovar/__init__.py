import os
from dotenv import load_dotenv

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()


def create_app():
    """Initialize core application."""
    app = Flask(__name__, instance_relative_config=False)

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # configuration with environmetnal variables from python-dotenv
    ENV_DIR = os.path.join(ROOT_DIR, '.env')
    load_dotenv(ENV_DIR)

    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'),
    )

    # Plugins
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    with app.app_context():
        from chemovar.strains import routes as strain_routes
        from chemovar.terpenes import routes as terpene_routes
        from chemovar.compounds import routes as compound_routes
        # Register Blueprints
        app.register_blueprint(strain_routes.strain_bp)
        app.register_blueprint(terpene_routes.terpene_bp)
        app.register_blueprint(compound_routes.compound_bp)

    return app
