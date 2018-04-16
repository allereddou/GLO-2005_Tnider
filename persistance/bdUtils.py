from Users import *
from persistance.passwordUtil import check_password, hash_password
from re import I, match

defaultPrefBird = {'birb': 1, 'blackBirb': 1, 'greenBirb': 1, '1_2WeightBirb': 1, 'maleBirb': 1, 'greyBirb': 1,
                   '10AgePlusBirb': 1,
                   'whiteBirb': 1, 'blueBirb': 1, '0_1WeightBirb': 1, '2PlusWeightBirb': 1, 'yellowBirb': 1,
                   '5_10AgeBirb': 1, 'femaleBirb': 1, 'beigeBirb': 1, '0_5AgeBirb': 1}
defaultPrefCat = {'cat': 1, 'declawedCat': 1, 'brownCat': 1, 'whiteCat': 1, '0_10WeightCat': 1, 'blackCat': 1,
                  'gingerCat': 1,
                  '0_5AgeCat': 1, '10_20WeightCat': 1, '10PlusAgeCat': 1, 'castratedCat': 1, '20PlusWeightCat': 1,
                  '5_10AgeCat': 1, 'maleGenderCat': 1, 'femaleGenderCat': 1, 'greyCat': 1}
defaultPrefDog = {'dog': 1, '0_20WeightDoggo': 1, '20_40WeightDoggo': 1, '5_10AgeDoggo': 1, 'whiteDoggo': 1,
                  'femaleGenderDoggo': 1, 'declawedDoggo': 1, '40WeightPlusDoggo': 1, '0_5AgeDoggo': 1,
                  'maleGenderDoggo': 1, 'brownDoggo': 1, 'castratedDoggo': 1, '10AgePlusDoggo': 1, 'gingerDoggo': 1,
                  'blackDoggo': 1, 'greyDoggo': 1}


def getUserFromEmail(email):
    from server import app, get_db
    with app.app_context():
        cursor = get_db()
        sql = "SELECT * FROM user WHERE email='{}';"
        cursor.execute(sql.format(email))
        user = cursor.fetchall()
        sql = "SELECT * FROM preferencesCat WHERE username = '{}'"
        cursor.execute(sql.format(user[0]['username']))
        prefCat = cursor.fetchall()[0]
        prefCat.pop('username', None)
        sql = "SELECT * FROM preferencesDog WHERE username = '{}'"
        cursor.execute(sql.format(user[0]['username']))
        prefDog = cursor.fetchall()[0]
        prefDog.pop('username', None)
        sql = "SELECT * FROM preferencesBird WHERE username = '{}'"
        cursor.execute(sql.format(user[0]['username']))
        prefBird = cursor.fetchall()[0]
        prefBird.pop('username', None)
        if len(user) != 1:
            return None
        return {**user[0], 'preferencesCat': prefCat, 'preferencesDog': prefDog, 'preferencesBird': prefBird}


def createUser(user):
    from server import app, get_db
    with app.app_context():
        cursor = get_db()

        sql = "INSERT INTO user(username, pass, nom, prenom, email, telephone, solde) VALUES ('{}', '{}', '{}', '{}', '{}', {}, {})"
        hashedPass = hash_password(user.password)
        cursor.execute(
            sql.format(user.username, hashedPass, user.nom, user.prenom, user.email, user.telephone, user.solde))

        sql = "INSERT INTO  preferencesDog(username, dog, whiteDoggo, blackDoggo, gingerDoggo, brownDoggo, greyDoggo, declawedDoggo, castratedDoggo, femaleGenderDoggo, maleGenderDoggo, 0_20WeightDoggo, 20_40WeightDoggo, 40WeightPlusDoggo, 0_5AgeDoggo, 5_10AgeDoggo, 10AgePlusDoggo) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
        cursor.execute(sql.format(user.username))

        sql = "INSERT INTO preferencesBird(username, birb, blackBirb, whiteBirb, blueBirb, beigeBirb, greyBirb, greenBirb, yellowBirb, 0_5AgeBirb, 5_10AgeBirb, 10AgePlusBirb, 0_1WeightBirb, 1_2WeightBirb, 2PlusWeightBirb, femaleBirb, maleBirb) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
        cursor.execute(sql.format(user.username))

        sql = "INSERT INTO preferencesCat(username, cat,declawedCat, whiteCat, blackCat, gingerCat, greyCat, brownCat, castratedCat,femaleGenderCat, maleGenderCat, 0_10WeightCat, 10_20WeightCat, 20PlusWeightCat, 0_5AgeCat, 5_10AgeCat, 10PlusAgeCat) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
        cursor.execute(sql.format(user.username))


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
    user.preferencesCat = {}
    user.preferencesDog = {}
    user.preferencesBird = {}

    preferences.pop('Save', None)

    # reset all prefs in bd cat
    for key in defaultPrefCat:
        sql = "UPDATE preferencesCat SET {} = 0 WHERE username='{}';"
        cursor.execute(sql.format(key, user.username))

    # reset all prefs in bd dog
    for key in defaultPrefDog:
        sql = "UPDATE preferencesDog SET {} = 0 WHERE username='{}';"
        cursor.execute(sql.format(key, user.username))

    # reset all prefs in bd bird
    for key in defaultPrefBird:
        sql = "UPDATE preferencesBird SET {} = 0 WHERE username='{}';"
        cursor.execute(sql.format(key, user.username))

    # set prefs
    for key, value in preferences.items():
        print(key)
        matchObjDog = match(r'.{0,}Doggo', key, I)
        matchObjCat = match(r'.{0,}Cat', key, I)
        matchObjBird = match(r'.{0,}Birb', key, I)

        if matchObjBird is not None and key is not 'birb':
            sql = "UPDATE preferencesBird SET {} = 1 WHERE username='{}';"
            cursor.execute(sql.format(key, user.username))
            user.preferencesBird[key] = 1
        elif matchObjCat is not None:
            sql = "UPDATE preferencesCat SET {} = 1 WHERE username='{}';"
            cursor.execute(sql.format(key, user.username))
            user.preferencesCat[key] = 1
        elif matchObjDog is not None:
            sql = "UPDATE preferencesDog SET {} = 1 WHERE username='{}';"
            cursor.execute(sql.format(key, user.username))
            user.preferencesDog[key] = 1
        else:
            print("key error")
