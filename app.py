import os
from dotenv import load_dotenv

from flask import (
    Flask,
    redirect,
    render_template,
    url_for
)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome

from forms import CompoundForm, SearchForm, TerpeneForm

app = Flask(__name__)
Bootstrap(app)
fa = FontAwesome(app)


# configuration with environmetnal variables from python-dotenv
# This is your Project Root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_DIR = os.path.join(ROOT_DIR, '.env')
load_dotenv(ENV_DIR)


headers = {
    'X-API-Key': os.getenv('CANNABIS_REPORTS_API'),
}

# set config variables based on flask environment setting
if app.config['ENV'] == 'development':
    app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'),
        )

db = SQLAlchemy(app)

migrate = Migrate(app, db)


# VIEW FUNCTIONS
def get_index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template("index.html", form=form)


def get_strain_list():
    strains = Strain.query.order_by(Strain.name.desc()).all()
    return render_template("strains.html", strains=strains)


def get_strain_object(id):
    strain = Strain.query.get_or_404(id)
    return render_template("strain.html", strain=strain)


def get_compound_list():
    compounds = Compound.query.all()
    return render_template("compounds.html", compounds=compounds)


def get_compound_object(id):
    compound = Compound.query.get_or_404(id)
    return render_template("compound.html", compound=compound)


def get_terpene_list():
    terpenes = Terpene.query.all()
    return render_template("terpenes.html", terpenes=terpenes)


# ROUTES
@app.route('/', methods=['GET'])
def index():
    return get_index()


@app.route('/strains/', methods=['GET'])
def strains():
    """
    RETURNS UNORDERED LIST OF STRAINS FROM THE DB.
    """
    return get_strain_list()


@app.route('/strains/<int:id>/', methods=['GET'])
def strain(id):
    """
    RETURNS STRAIN INSTANCE DETAIL TEMPLATE.
    """
    return get_strain_object(id)


@app.route('/compounds/', methods=['GET'])
def compounds():
    """
    RETURNS LIST OF COMPOUND INSTANCES FROM DB.
    """
    return get_compound_list()


@app.route('/compound/<int:id>/', methods=['GET'])
def compound(id):
    """
    RETURN COMPOUND INSTANCE FROM DB.
    """
    return get_compound_object(id)


@app.route('/terpenes/', methods=['GET'])
def terpenes():
    """
    RETURN LIST OF TERPENE INSTANCES.
    """
    return get_terpene_list()


@app.route('/compounds/add/', methods=['GET', 'POST'])
def compound_add():
    form = CompoundForm()
    # conveience method check if POST and form valid
    if form.validate_on_submit():
        compound = Compound()
        compound.name = form.name.data
        db.session.add(compound)
        db.session.commit()
        return redirect(url_for('compounds.html'))
    return render_template('compound_form.html', form=form)


@app.route('/terpenes/add/', methods=['GET', 'POST'])
def terpene_add():
    form = TerpeneForm()
    # conveience method check if POST and form valid
    if form.validate_on_submit():
        terpene = Terpene()
        terpene.compound_id = form.compound_id.data
        db.session.add(terpene)
        db.session.commit()
        return redirect(url_for('terpenes'))
    return render_template('terpene_form.html', form=form)


if __name__ == '__main__':
    app.run()


from models import Compound, Terpene, Strain
