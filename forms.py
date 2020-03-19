
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectMultipleField
)


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
    submit = SubmitField()