from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, widgets
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
    password2 = PasswordField('Password', validators=[DataRequired(), Length(max=100), equal_to('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('confirm password', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired(), Length(max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=20)])
    phone_number = IntegerField("Phone Number", widget=widgets.Input(input_type="tel"), validators=[DataRequired()])
    register = SubmitField('submit')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(RegisterForm, self).__init__(*args, **kwargs)







