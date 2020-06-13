import os
from dotenv import load_dotenv

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from flask_security import Security, SQLAlchemySessionUserDatastore

# Global libraries
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()


# Flask-Security
security = Security()


def create_app():
    """Initialize core application."""
    app = Flask(__name__, instance_relative_config=False)

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # configuration with environmetnal variables
    ENV_DIR = os.path.join(ROOT_DIR, '.env')
    load_dotenv(ENV_DIR)

    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'),
        SECURITY_PASSWORD_SALT=os.getenv('SECURITY_PASSWORD_SALT'),
        SECURITY_REGISTERABLE=True,
    )

    # Initialize plugins
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    from chemovar.users.models import User, Role

    user_datastore = SQLAlchemySessionUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_blueprint=True)

    with app.app_context():
        # Import models
        from chemovar.compounds.models import Compound
        from chemovar.terpenes.models import Terpene
        from chemovar.strains.models import Strain
        from chemovar.assays.models import Assay
        from chemovar.strains import routes as strain_routes
        from chemovar.terpenes import routes as terpene_routes
        from chemovar.compounds import routes as compound_routes
        # Register Blueprints
        app.register_blueprint(strain_routes.strain_bp)
        app.register_blueprint(terpene_routes.terpene_bp)
        app.register_blueprint(compound_routes.compound_bp)

    return app