from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    content = StringField('Query', validators=[DataRequired()])
    submit = SubmitField('Search')
