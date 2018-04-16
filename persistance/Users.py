from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from persistance.bdUtils import getUserFromEmail


class User(UserMixin):
    def __init__(self, email, password, username, nom, prenom, telephone, solde, profileImage, preferencesBird, preferencesCat, preferencesDog):
        self.email = email
        self.password = password
        self.username = username
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.solde = solde
        self.profileImage = profileImage
        self.preferencesDog = preferencesDog
        self.preferencesCat = preferencesCat
        self.preferencesBird = preferencesBird

    def get_auth_token(self):
        from server import app
        login_serializer = URLSafeTimedSerializer(app.secret_key)
        data = [str(self.email), self.password]
        return login_serializer.dumps(data)

    @staticmethod
    def get(email):
        from server import app
        with app.app_context():
            result = getUserFromEmail(email)

            if not result:
                return None
            else:
                password = (result['pass'])
            return User(email, password, result['username'], result['nom'], result['prenom'], result['telephone'],
                        result['solde'], result['profileImage'], result['preferencesBird'], result['preferencesCat'], result['preferencesDog'])

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email
