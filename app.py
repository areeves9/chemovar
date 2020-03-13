import os
from dotenv import load_dotenv

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome

from forms import SearchForm

app = Flask(__name__)
Bootstrap(app)
fa = FontAwesome(app)


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


# VIEW FUNCTIONS
def get_index():
    form = SearchForm()
    if form.validate_on_submit():
        flash('Search for strain {} success!'.format(
            form.strain.data))
        return redirect(url_for('success'))
    return render_template('index.html', form=form)


def get_search_results(data):
    strain = data
    search_strain_terpenes = db.session.query(Compound.name).\
        join("terpenes", "strains").\
        filter(Strain.name == strain).\
        subquery()

    result = db.session.query(Strain).\
        join("terpenes", "compound").\
        filter(Compound.name.in_(search_strain_terpenes)).\
        group_by(Strain.id).\
        having(db.func.count() >= 2).\
        all()

    count = len(result)

    return render_template(
        'success.html',
        count=count,
        results=result,
        strain=strain
    )


def get_strain_list():
    results = Strain.query.order_by(Strain.name.desc()).all()
    count = len(results)
    return render_template(
        "strains.html",
        count=count,
        results=results,
    )


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


@app.route('/success', methods=['GET', 'POST'])
def success():
    data = request.form['strain']
    return get_search_results(data)


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


if __name__ == '__main__':
    app.run()

from models import Compound, Terpene, Strain
