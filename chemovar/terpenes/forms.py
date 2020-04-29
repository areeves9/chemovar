from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField,
)
from wtforms.validators import DataRequired


class TerpeneForm(FlaskForm):
    aroma = SelectField(
         'aroma',
         choices=[
             ('Sweet', 'Sweet'),
             ('Woody', 'Woody'),
             ('Citrus', 'Citrus'),
             ('Pepper', 'Pepper'),
             ('Herbal', 'Herbal'),
             ('Pine', 'Pine'),
             ('Rosy', 'Rosy'),
             ('Floral', 'Floral'),
             ('Earthy', 'Earthy'),
             ('Fruity', 'Fruity'),
             ('Musky', 'Musky'),
             ('Skunky', 'Skunky'),
            ]
     )
    compound_id = SelectField(coerce=int)
    submit = SubmitField()