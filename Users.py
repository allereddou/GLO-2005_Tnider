from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer


class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password

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
            return User(email, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email
