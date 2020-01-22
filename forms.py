from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired


class CompoundForm(FlaskForm):
    """
    A FORM FOR CREATING A COMPOUND.
    """
    name = StringField('name', validators=[DataRequired()])
    percent_concentration = DecimalField('percent_concentration', places=3, validators=[DataRequired()])