from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class PreferenceForm(FlaskForm):
    save = SubmitField('submit')
    kitteh1 = BooleanField('kitteh')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(PreferenceForm, self).__init__(*args, **kwargs)
