from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from persistance.bdUtils import getUserFromEmail

defaultProfileImage = "https://accrualnet.cancer.gov/sites/accrualnet.cancer.gov/themes/accrualnet/accrualnet-internals/images/avatars/male/Red.png"

defaultPrefBird = {'birb': 1, 'blackBirb': 1, 'greenBirb': 1, '1_2WeightBirb': 1, 'maleBirb': 1, 'greyBirb': 1,
                   '10AgePlusBirb': 1,
                   'whiteBirb': 1, 'blueBirb': 1, '0_1WeightBirb': 1, '2PlusWeightBirb': 1, 'yellowBirb': 1,
                   '5_10AgeBirb': 1, 'femaleBirb': 1, 'beigeBirb': 1, '0_5AgeBirb': 1}
defaultPrefCat = {'kitteh': 1, 'declawedCat': 1, 'brownCat': 1, 'whiteCat': 1, '0_10WeightCat': 1, 'blackCat': 1,
                  'gingerCat': 1,
                  '0_5AgeCat': 1, '10_20WeightCat': 1, '10PlusAgeCat': 1, 'castratedCat': 1, '20PlusWeightCat': 1,
                  '5_10AgeCat': 1, 'maleGenderCat': 1, 'femaleGenderCat': 1, 'greyCat': 1}
defaultPrefDog = {'dog': 1, '0_20WeightDoggo': 1, '20_40WeightDoggo': 1, '5_10AgeDoggo': 1, 'whiteDoggo': 1,
                  'femaleGenderDoggo': 1, 'declawedDoggo': 1, '40WeightPlusDoggo': 1, '0_5AgeDoggo': 1,
                  'maleGenderDoggo': 1, 'brownDoggo': 1, 'castratedDoggo': 1, '10AgePlusDoggo': 1, 'gingerDoggo': 1,
                  'blackDoggo': 1, 'greyDoggo': 1}


class User(UserMixin):
    def __init__(self, email, password, username, nom, prenom, telephone, solde, profileImage):
        self.email = email
        self.password = password
        self.username = username
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.solde = solde
        self.profileImage = profileImage
        self.preferencesDog = defaultPrefDog
        self.preferencesCat = defaultPrefCat
        self.preferencesBird = defaultPrefBird

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
                        result['solde'], result['profileImage'])

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email
