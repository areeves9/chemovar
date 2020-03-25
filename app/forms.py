from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField,
    SelectMultipleField,
    widgets
)
from wtforms.validators import DataRequired
from app.models import Terpene


class CompoundForm(FlaskForm):
    """
    A FORM FOR CREATING A COMPOUND.
    """
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField()


class TerpeneForm(FlaskForm):
    aroma = StringField('aroma', validators=[DataRequired()])
    compound_id = SelectField(coerce=int)
    submit = SubmitField()


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