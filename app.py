import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

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

from models import Compound, Terpene, Strain

migrate = Migrate(app, db)


def get_strain_list():
    strains = Strain.query.order_by(Strain.name.desc()).all()
    return render_template("strains.html", strains=strains)


def get_strain_object(id):
    strain = Strain.query.get_or_404(id)
    # strain_html = f'<h3>{strain.name}</h3>'.format(strain.name)
    return render_template("strain.html", strain=strain)


@app.route('/strains/', methods=['GET'])
def strains():
    if request.method == 'GET':
        return get_strain_list()


@app.route('/strains/<int:id>/', methods=['GET'])
def strain(id):
    if request.method == 'GET':
        return get_strain_object(id)


if __name__ == '__main__':
    app.run()