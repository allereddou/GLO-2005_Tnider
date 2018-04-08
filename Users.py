from flask_login import UserMixin
from flask import g


class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.authenticated = False
        self.validateLogin()

    def is_authenticated(self):
        return self.authenticated

    def validateLogin(self):
        from server import app, get_db
        with app.app_context():

            cursor = get_db()

            sql = "SELECT * FROM user WHERE email='{}';"
            cursor.execute(sql.format(self.email))

            result = cursor.fetchall()
            print(result[0]['email'])

            return len(result) != 0 and result[0]['pass'] == self.password
