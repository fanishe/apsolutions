from wtforms import Form, StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = StringField('Datasearch', validators = [DataRequired()])
