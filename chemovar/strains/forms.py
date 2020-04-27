from chemovar.terpenes.models import Terpene
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    SelectMultipleField,
    widgets
)


class SearchForm(FlaskForm):
    strain = StringField('Search')
    submit = SubmitField()


class StrainForm(FlaskForm):
    name = StringField('')
    terpenes = SelectMultipleField(
        'Terpene',
        coerce=int,
        widget=widgets.ListWidget(prefix_label=True),
        option_widget=widgets.CheckboxInput())
    submit = SubmitField()

    def set_choices(self):
        self.terpenes.choices = [(d.id, d.compound.name) for d in Terpene.query.all()]
