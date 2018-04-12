from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class PreferenceForm(FlaskForm):
    Save = SubmitField('submit')
    blackBirb = BooleanField('blackBirb')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(PreferenceForm, self).__init__(*args, **kwargs)
