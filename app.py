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

from forms import CompoundForm, SearchForm, TerpeneForm, StrainForm


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


# VIEW FUNCTIONS
def get_index():
    form = SearchForm()
    if form.validate_on_submit():
        flash('Search for strain {} success!'.format(
            form.strain.data))
        return redirect(url_for('success'))
    return render_template('index.html', form=form)


def create_compound():
    form = CompoundForm()
    if form.validate_on_submit():
        compound = Compound()
        compound.name = form.data['name']
        db.session.add(compound)
        db.session.commit()
        return redirect(url_for('compounds'))
    return render_template('compound_form.html', form=form)


def create_terpene():
    form = TerpeneForm()
    form.compound_id.choices = [(c.id, c.name) for c in Compound.query.all()]

    if form.validate_on_submit():
        terpene = Terpene()
        terpene.compound_id = form.data['compound_id']
        terpene.aroma = form.data['aroma']
        db.session.add(terpene)
        db.session.commit()
        return redirect(url_for('terpenes'))
    return render_template('terpene_form.html', form=form)


def create_strain():
    form = StrainForm()

    if form.validate_on_submit():
        strain = Strain()
        strain.name = form.data['name']
        db.session.add(strain)
        db.session.commit()
        return redirect(url_for('strains'))
    return render_template('strain_form.html', form=form)


def get_search_results(data):
    strain = data
    search_strain_terpenes = db.session.query(Compound.name).\
        join("terpenes", "strains").\
        filter(Strain.name.ilike(strain)).\
        subquery()

    result = db.session.query(Strain).\
        join("terpenes", "compound").\
        filter(Compound.name.in_(search_strain_terpenes)).\
        group_by(Strain.id).\
        having(db.func.count() >= 3).\
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
    aromas = []
    countries = []
    codes = []
    image = strain.image
    lineage = strain.lineage
    terpenes = []

    for key in lineage:
        codes.append((lineage[key]).upper())
        countries.append(key)

    for terpene in strain.terpenes:
        aromas.append(terpene.aroma)
        terpenes.append(terpene.compound.name)

    return render_template(
        "strain.html",
        aromas=aromas,
        image=image,
        codes=codes,
        lineage=[lineage],
        strain=strain,
        terpenes=terpenes,
    )


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


@app.route('/strains/add/', methods=['GET', 'POST'])
def add_strain():
    """
    CREATE A COMPOUND AND SAVE TO THE DB.
    """
    return create_strain()


@app.route('/compounds/add/', methods=['GET', 'POST'])
def add_compound():
    """
    CREATE A COMPOUND AND SAVE TO THE DB.
    """
    return create_compound()


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


@app.route('/terpenes/add/', methods=['GET', 'POST'])
def add_terpene():
    return create_terpene()


if __name__ == '__main__':
    app.run()

from models import Compound, Terpene, Strain
