from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField,
)
from wtforms.validators import DataRequired


class TerpeneForm(FlaskForm):
    aroma = StringField('aroma', validators=[DataRequired()])
    compound_id = SelectField(coerce=int)
    submit = SubmitField()