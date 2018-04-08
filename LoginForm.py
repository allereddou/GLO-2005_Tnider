from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import pymysql


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

    def validate(self, user, password):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root')

        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "USE PROJET_BD"
        cursor.execute(sql)

        sql = "SELECT * FROM user WHERE username = '{}'"
        cursor.execute(sql.format(user))







