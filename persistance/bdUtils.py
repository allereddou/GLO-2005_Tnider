from Users import *
from persistance.passwordUtil import check_password, hash_password



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

    for key, value in preferences.items():
        sql = "UPDATE preferences SET {} = 1 WHERE username='{}';"
        cursor.execute(sql.format(key, user.username))
        user.preferences[key] = 1

    return user.preferences


def setDefaultPreferences(user):
    from server import get_db

    cursor = get_db()



