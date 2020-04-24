from .models import Compound
from .forms import CompoundForm
from flask import (
    redirect,
    render_template,
    url_for
)

# VIEW FUNCTIONS


def create_compound():
    form = CompoundForm()
    if form.validate_on_submit():
        compound = Compound()
        compound.name = form.data['name']
        db.session.add(compound)
        db.session.commit()
        return redirect(url_for('compounds'))
    return render_template('forms/compound_form.html', form=form)


def get_compound_list():
    compounds = Compound.query.all()
    return render_template("compounds.html", compounds=compounds)


def get_compound_object(id):
    compound = Compound.query.get_or_404(id)
    return render_template("compound.html", compound=compound)


