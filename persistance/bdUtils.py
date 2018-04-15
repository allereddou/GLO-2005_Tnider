from Users import *
from persistance.passwordUtil import check_password, hash_password

defaultPref = {'blackBirb': 1, '0_10CatWeight': 1, '5_10AgeDoggo': 1, 'blackCat': 1, 'whiteDoggo': 1, 'greenBirb': 1,
               'femaleGenderDoggo': 1, 'gingerCat': 1, '0_5CatAge': 1, '10_20CatWeight': 1, 'declawedDoggo': 1,
               '10PlusCatAge': 1, '1_2WeightBirb': 1, 'maleBirb': 1, '40WeightPlusDoggo': 1, '0_5AgeDoggo': 1,
               'greyBirb': 1, '10AgePlusBirb': 1, 'maleGenderDoggo': 1, 'castratedCat': 1, 'whiteBirb': 1,
               '20PlusCatWeight': 1, '5_10CatAge': 1, 'brownDoggo': 1, 'castratedDoggo': 1, '10AgePlusDoggo': 1,
               'whiteCat': 1, 'blueBirb': 1, '0_1WeightBirb': 1, '20_40WeightDoggo': 1, 'brownCat': 1, 'beigeBirb': 1,
               'maleGenderCat': 1, 'femaleGenderCat': 1, 'greyCat': 1, '0_5AgeBirb': 1, '0_20WeightDoggo': 1,
               'gingerDoggo': 1, 'blackDoggo': 1, 'greyDoggo': 1, '2PlusWeightBirb': 1, 'yellowBirb': 1,
               '5_10AgeBirb': 1, 'femaleBirb': 1, 'declawedCat': 1}


def getUserFromEmail(email):
    from server import app, get_db
    with app.app_context():
        cursor = get_db()

        sql = "SELECT * FROM user WHERE email='{}';"
        cursor.execute(sql.format(email))
        result = cursor.fetchall()

        if len(result) != 1:
            return None
        return result[0]


def createUser(user):
    from server import app, get_db
    with app.app_context():
        cursor = get_db()

        sql = "INSERT INTO user(username, pass, nom, prenom, email, telephone, solde) VALUES ('{}', '{}', '{}', '{}', '{}', {}, {})"
        hashedPass = hash_password(user.password)
        cursor.execute(
            sql.format(user.username, hashedPass, user.nom, user.prenom, user.email, user.telephone, user.solde))


def checkIfUsernameAlreadyUsed(username):
    from server import get_db
    cursor = get_db()
    sql = "SELECT username FROM user"
    cursor.execute(sql)
    results = cursor.fetchall()

    for i in results:
        if i['username'] == username:
            return False
    return True


def checkIfEmailAlreadyUsed(email):
    from server import get_db
    cursor = get_db()
    sql = "SELECT email FROM user"
    cursor.execute(sql)
    results = cursor.fetchall()

    for i in results:
        if i['email'] == email:
            return False
    return True


def validatePassword(email, password):
    from server import get_db
    cursor = get_db()
    sql = "SELECT pass FROM user WHERE email='{}'"
    cursor.execute(sql.format(email))
    result = cursor.fetchall()

    print(result)
    if result is None:
        return None

    if check_password(result[0]['pass'], password):
        print("right pass")
        return True
    else:
        print("wrong pass")
        return False


def updatePreferences(user, preferences):
    from server import get_db

    cursor = get_db()
    user.preferences = {}

    try:
        del preferences['Save']
    except KeyError:
        pass

    # reset all prefs in bd
    for key in defaultPref:
        sql = "UPDATE preferences SET {} = 0 WHERE username='{}';"
        cursor.execute(sql.format(key, user.username))

    # set prefs to 1
    for key, value in preferences.items():
        sql = "UPDATE preferences SET {} = 1 WHERE username='{}';"
        cursor.execute(sql.format(key, user.username))
        user.preferences[key] = 1

    return user.preferences
