from .models import Strain
from .forms import SearchForm, StrainForm
from chemovar.compounds.models import Compound

from chemovar import db
from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for
)

strain_bp = Blueprint('strain_bp', __name__,
                        template_folder='templates',
                        static_folder='static')


def get_autocomplete():
    strains = Strain.query.all()
    list_strains = [s.serialize for s in strains]
    return jsonify(list_strains)


def get_index():
    form = SearchForm()
    if form.validate_on_submit():
        flash('Search for strain {} success!'.format(
            form.strain.data))
        return redirect(url_for('strain_bp.success'))
    return render_template('index.html', form=form)


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
        return redirect(url_for('strain_bp.strains'))
    return render_template('forms/strain_form.html', form=form)


def get_search_results(strain=None):
    search_strain_terpenes = db.session.query(Compound.name).\
        join("terpenes", "strains").\
        filter(Strain.name.ilike(strain)).\
        subquery()

    results = db.session.query(Strain).\
        join("terpenes", "compound").\
        filter(Compound.name.in_(search_strain_terpenes)).\
        filter(Strain.name.notin_([strain])).\
        group_by(Strain.id).\
        having(db.func.count() >= 5).all()

    print(results)

    return render_template(
        'success.html',
        results=results,
        count=len(results),
        strain=strain,
    )


def get_strain_list(page=1):
    if request.args:
        page = request.args.get('page', 1, type=int)
    per_page = 10
    results = Strain.query.order_by(Strain.name.desc()).paginate(page, per_page)
    return render_template(
        "strains.html",
        count=results.total,
        results=results,
        current_page=page,
        pages=results.pages,
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

    return render_template(
        "strain.html",
        aromas=aromas[:4],
        image=image,
        codes=codes,
        lineage=[lineage],
        strain=strain,
        terpenes=terpenes,
    )
