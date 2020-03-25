import os
from dotenv import load_dotenv

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


# configuration with environmetnal variables from python-dotenv
# This is your Project Root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_DIR = os.path.join(ROOT_DIR, '.env')
load_dotenv(ENV_DIR)



# set config variables based on flask environment setting
if app.config['ENV'] == 'development':
    app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'),
        )

db = SQLAlchemy(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()