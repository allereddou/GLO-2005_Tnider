from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, equal_to, Length


class LoginForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])
    login = SubmitField('submit')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(LoginForm, self).__init__(*args, **kwargs)


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(max=100), equal_to('confirmPassword', message='Passwords must match')])
    confirmPassword = PasswordField('confirmPassword', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired(), Length(max=20)])
    first_name = StringField('lastName', validators=[DataRequired(), Length(max=20)])
    last_name = StringField('lastName', validators=[DataRequired(), Length(max=20)])
    register = SubmitField('submit')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(RegisterForm, self).__init__(*args, **kwargs)





