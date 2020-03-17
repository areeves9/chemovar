from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class CompoundForm(FlaskForm):
    """
    A FORM FOR CREATING A COMPOUND.
    """
    name = StringField('name', validators=[DataRequired()])


class TerpeneForm(FlaskForm):
    aroma = StringField('aroma', validators=[DataRequired()])
    compound_id = SelectField(coerce=int)


class SearchForm(FlaskForm):
    strain = StringField('Search')
    submit = SubmitField()