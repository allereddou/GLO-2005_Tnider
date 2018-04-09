from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from persistance.passwordUtil import hash_password


class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password

      #  self.validateLogin()

    # def validateLogin(self):
    #     from server import app, get_db
    #     with app.app_context():
    #         cursor = get_db()
    #
    #         sql = "SELECT * FROM user WHERE email='{}';"
    #         cursor.execute(sql.format(self.email))
    #         result = cursor.fetchall()
    #         return len(result) != 0 and result[0]['pass'] == self.password

    def get_auth_token(self):
        login_serializer = URLSafeTimedSerializer(app.secret_key)
        data = [str(self.email), self.password]
        return login_serializer.dumps(data)

    @staticmethod
    def get(email):
        from server import app, get_db
        with app.app_context():
            cursor = get_db()

            sql = "SELECT * FROM user WHERE email='{}';"
            cursor.execute(sql.format(email))
            result = cursor.fetchall()

            if len(result) == 0:
                return None
            else:
                password = (result[0]['pass'])
                print("password: " + password)
            return User(email, password)
