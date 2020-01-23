from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField
from wtforms.validators import DataRequired



class CompoundForm(FlaskForm):
    """
    A FORM FOR CREATING A COMPOUND.
    """
    name = StringField('name', validators=[DataRequired()])
    percent_concentration = DecimalField('percent_concentration', places=3, validators=[DataRequired()])


class TerpeneForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    compound_id = SelectField(coerce=int)
