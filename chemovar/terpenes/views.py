from chemovar import db
from chemovar.compounds.models import Compound
from chemovar.terpenes.models import Terpene
from chemovar.terpenes.forms import TerpeneForm
from flask import (
    redirect,
    render_template,
    url_for
)
# VIEW FUNCTIONS


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


def get_terpene_list():
    terpenes = Terpene.query.all()
    return render_template("terpenes.html", terpenes=terpenes)
