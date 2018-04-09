from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    password = StringField('password', validators=[DataRequired()])









