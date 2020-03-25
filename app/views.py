from app.models import Compound, Terpene, Strain
from app.forms import CompoundForm, TerpeneForm, SearchForm, StrainForm
from app.app import app, db
from flask import (
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for
)

# VIEW FUNCTIONS


def get_autocomplete():
    strains = Strain.query.all()
    list_strains = [s.serialize for s in strains]
    return jsonify(list_strains)


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
    return render_template('forms/compound_form.html', form=form)


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
    return render_template('forms/terpene_form.html', form=form)


def create_strain():
    form = StrainForm()
    form.set_choices()

    if form.validate_on_submit():
        strain = Strain()
        strain.name = form.data['name']
        terps = []
        for t in form.data['terpenes']:
            f = Terpene.query.get(str(t))
            print(f)
            terps.append(f)
        print(terps)
        strain.terpenes.extend(terps)
        strain.get_strain_data()
        db.session.add(strain)
        db.session.commit()
        return redirect(url_for('strains'))
    return render_template('forms/strain_form.html', form=form)


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

    # iterate through query results, checking ea. object
    # to see if it is True, and return a list of all
    # True objects
    filteredResult = list(
        filter(
            None, map(
                lambda obj: None if obj.name.lower()
                == strain.lower() else obj, result)
            )
        )

    count = len(filteredResult)

    return render_template(
        'success.html',
        count=count,
        results=filteredResult,
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

    if lineage:
        for key in lineage:
            codes.append((lineage[key]).upper())
            countries.append(key)
    else:
        pass

    for terpene in strain.terpenes:
        aromas.append(terpene.aroma)
        terpenes.append(terpene.compound.name)
    # x = slice(4)
    # aromas = aromas[x]

    print(aromas)

    return render_template(
        "strain.html",
        aromas=aromas[:4],
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


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    return get_autocomplete()


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