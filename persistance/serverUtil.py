import pymysql
from flask import g
import random
from persistance.passwordUtil import hash_password

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


def get_db():
    sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'PROJET_BD';"

    if not hasattr(g, 'cursor'):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             autocommit=True)

        g.cursor = db.cursor(pymysql.cursors.DictCursor)
        schemaExists = g.cursor.execute(sql)

        if not schemaExists:
            sql = "CREATE DATABASE IF NOT EXISTS PROJET_BD"
            g.cursor.execute(sql)

        g.cursor.execute("USE PROJET_BD")
    return g.cursor


def findMyAnimals(user):
    cursor = get_db()
    cursor.execute(
        "SELECT P.link, A.nom, A.id, A.race, A.sexe, A.poids, A.age, V.prix, A.location, A.description FROM vend V, animal A, pic P WHERE V.username = '{}' and V.id_animal = A.id and P.id = A.id".format(
            user.username))
    tosell = cursor.fetchall()
    myanimals = []
    for animal in tosell:
        if animal['race'] == 'Kitteh':
            cursor.execute("SELECT pelage, castre, degriffe, sousrace FROM cat WHERE id = {}".format(animal['id']))
        elif animal['race'] == 'Doggo':
            cursor.execute("SELECT pelage, castre, degriffe, sousrace FROM dog WHERE id = {}".format(animal['id']))
        elif animal['race'] == 'Birb':
            cursor.execute("SELECT plumage, sousrace FROM bird WHERE id = {}".format(animal['id']))
        race = cursor.fetchall()[0]
        myanimals.append({**animal, **race, 'activeID': str(animal['id'])})
    return myanimals


def deleteAnimalFromBD(num):
    cursor = get_db()
    cursor.execute("DELETE FROM animal WHERE id = {}".format(num))
    try:
        cursor.execute("SELECT * FROM animal WHERE id = {}".format(num))
    except:
        return False
    return True


def likeAnimal(ID):
    cursor = get_db()
    cursor.execute("INSERT desire(username, id) VALUES ('{}', {})".format(user.username, ID))


def dislikeAnimal(ID):
    cursor = get_db()
    cursor.execute("INSERT notdesired(username, id) VALUES ('{}', {})".format(user.username, ID))


def deleteNotDesiredinBD(user):
    cursor = get_db()
    cursor.execute("DELETE FROM notdesired WHERE username = '{}'".format(user.username))


def deleteDesiredinBD(num, user):
    cursor = get_db()
    cursor.execute(
        "DELETE FROM desire WHERE username = '{}' and id = {}".format(user.username, num))


def buyAnimalAndCleanBD(num, user):
    cursor = get_db()
    cursor.execute("SELECT * FROM vend WHERE id_animal = {}".format(num))
    vend = cursor.fetchall()[0]
    user.solde -= vend['prix']
    cursor.execute("UPDATE user SET solde = {} WHERE username = '{}'".format(user.solde, user.username))
    cursor.execute(
        "INSERT transactions(seller, id, buyer, prix) VALUES('{}',{},'{}',{})".format(vend['username'], num,
                                                                                      user.username,
                                                                                      vend['prix']))
    cursor.execute("DELETE FROM desire WHERE id = {}".format(num))
    cursor.execute("DELETE FROM notdesired WHERE id = {}".format(num))
    cursor.execute("DELETE FROM vend WHERE id_animal = {}".format(num))


def getTransactions(user):
    cursor = get_db()
    cursor.execute(
        "SELECT T.buyer, T.seller, A.nom FROM transactions T, animal A WHERE T.seller = '{}' and A.id = T.id".format(
            user.username))
    sold = cursor.fetchall()

    cursor = get_db()
    cursor.execute(
        "SELECT T.buyer, T.seller, A.nom FROM transactions T, animal A WHERE T.buyer = '{}' and A.id = T.id".format(
            user.username))
    bought = cursor.fetchall()
    return sold, bought


def changeUserinBD(user, field, new):
    cursor = get_db()
    if field == 'telephone' and isinstance(new, int):
        cursor.execute("UPDATE user SET {} = {} WHERE username = '{}'".format(field, new, user.username))
    elif field == 'pass':
        new = hash_password(new)
        cursor.execute("UPDATE user SET {} = '{}' WHERE username = '{}'".format(field, new, user.username))
    else:
        cursor.execute("UPDATE user SET {} = '{}' WHERE username = '{}'".format(field, new, user.username))


def changeUserImginBD(user, field, new):
    cursor = get_db()
    cursor.execute("UPDATE user SET {} = '{}' WHERE username = '{}'".format(field, new, user.username))


def changeAnimalinBD(ID, field, new):
    cursor = get_db()
    cursor.execute("SELECT race FROM animal WHERE id = {}".format(ID))
    race = cursor.fetchall()[0]['race']
    if field == 'color':
        if race == 'Doggo':
            cursor.execute("UPDATE dog SET pelage = '{}' WHERE id = {}".format(new, ID))
        elif race == 'Kitteh':
            cursor.execute("UPDATE cat SET pelage = '{}' WHERE id = {}".format(new, ID))
        elif race == 'Birb':
            cursor.execute("UPDATE bird SET plumage = '{}' WHERE id = {}".format(new, ID))
    elif field == 'prix':
        cursor.execute("UPDATE vend SET prix = {} WHERE id_animal = {}".format(new, ID))
    elif field == 'sousrace':
        if race == 'Doggo':
            cursor.execute("UPDATE dog SET sousrace = '{}' WHERE id = {}".format(new, ID))
        elif race == 'Kitteh':
            cursor.execute("UPDATE cat SET sousrace = '{}' WHERE id = {}".format(new, ID))
        elif race == 'Birb':
            cursor.execute("UPDATE bird SET sousrace = '{}' WHERE id = {}".format(new, ID))
    else:
        cursor.execute("UPDATE animal SET {} = '{}' WHERE id = {}".format(field, new, ID))


def changeAnimalOtherinBD(ID, castre, degriffe):
    cursor = get_db()
    cursor.execute("SELECT race FROM animal WHERE id = {}".format(ID))
    race = cursor.fetchall()[0]['race']
    if castre == 'true':
        if race == 'Doggo':
            cursor.execute("UPDATE dog SET castre = 1 WHERE id = {}".format(ID))
        elif race == 'Kitteh':
            cursor.execute("UPDATE cat SET castre = 1 WHERE id = {}".format(ID))
    if degriffe == 'true':
        if race == 'Doggo':
            cursor.execute("UPDATE dog SET degriffe = 1 WHERE id = {}".format(ID))
        elif race == 'Kitteh':
            cursor.execute("UPDATE cat SET degriffe = 1 WHERE id = {}".format(ID))
    if castre == 'false':
        if race == 'Doggo':
            cursor.execute("UPDATE dog SET castre = 0 WHERE id = {}".format(ID))
        elif race == 'Kitteh':
            cursor.execute("UPDATE cat SET castre = 0 WHERE id = {}".format(ID))
    if degriffe == 'false':
        if race == 'Doggo':
            cursor.execute("UPDATE dog SET degriffe = 0 WHERE id = {}".format(ID))
        elif race == 'Kitteh':
            cursor.execute("UPDATE cat SET degriffe = 0 WHERE id = {}".format(ID))


def changeAnimalImginBD(ID, new):
    cursor = get_db()
    cursor.execute("UPDATE pic SET link = '{}' WHERE id = {}".format(new, ID))


def getUser(username):
    cursor = get_db()
    cursor.execute(
        "SELECT U.username, U.nom, U.prenom, U.nom, U.email, U.profileImage, U.telephone FROM user U WHERE U.username = '{}'".format(
            username))
    return cursor.fetchall()[0]


def get_animals_desired(user):
    cursor = get_db()
    cursor.execute("SELECT D.id FROM desire D WHERE D.username = '{}'".format(user.username))
    id_wishlist = cursor.fetchall()
    wishlist = []
    for current_id in id_wishlist:
        cursor.execute(
            "SELECT DISTINCT A.id, P.link, A.sexe, A.age, A.poids, A.description, A.nom, A.race, A.location, V.username, V.prix FROM pic P, animal A, vend V WHERE A.id = V.id_animal and A.id = P.id and A.id = {};".format(
                current_id['id']))
        animal = cursor.fetchall()[0]
        if animal['race'] == 'Kitteh':
            cursor.execute("SELECT pelage, castre, degriffe, sousrace FROM cat WHERE id = {}".format(animal['id']))
        elif animal['race'] == 'Doggo':
            cursor.execute("SELECT pelage, castre, degriffe, sousrace FROM dog WHERE id = {}".format(animal['id']))
        elif animal['race'] == 'Birb':
            cursor.execute("SELECT plumage, sousrace FROM bird WHERE id = {}".format(animal['id']))
        race = cursor.fetchall()[0]
        wishlist.append({**animal, **race})
    return wishlist


def get_possible_match(user):
    cursor = get_db()
    sql = "SELECT A.id FROM animal A WHERE A.id not in (SELECT D.id FROM desire D WHERE D.username = '{}') and A.id not in (SELECT D.id FROM notdesired D WHERE D.username = '{}') and A.id not in (SELECT T.id FROM transactions T) and A.id not in (SELECT V.id_animal FROM vend V WHERE V.username = '{}');".format(
        user.username, user.username, user.username)
    cursor.execute(sql)
    possible_id = cursor.fetchall()

    # filter based on personal preferences
    possible_id = filterIds(possible_id)

    IDs = list()
    for i in possible_id:
        IDs.append(i['id'])
    random.shuffle(IDs)
    sql = "SELECT DISTINCT A.id, P.link, A.nom, A.race, A.location, A.sexe, A.age, A.poids, A.description FROM pic P, animal A WHERE A.id = P.id and A.id = {}".format(
        IDs.pop())
    cursor.execute(sql)
    animal = cursor.fetchall()[0]
    if animal['race'] == 'Kitteh':
        cursor.execute("SELECT pelage, castre, degriffe, sousrace FROM cat WHERE id = {}".format(animal['id']))
    elif animal['race'] == 'Doggo':
        cursor.execute("SELECT pelage, castre, degriffe, sousrace FROM dog WHERE id = {}".format(animal['id']))
    elif animal['race'] == 'Birb':
        cursor.execute("SELECT plumage, sousrace FROM bird WHERE id = {}".format(animal['id']))
    race = cursor.fetchall()[0]
    cursor.execute("SELECT prix FROM vend WHERE id_animal = {}".format(animal['id']))
    prix = cursor.fetchall()[0]
    return {**animal, **race, **prix}


def filterIds(possible_id):
    cursor = get_db()
    goodIds = []

    # filtre chien
    sql = "SELECT * FROM preferencesDog WHERE username='{}';"
    cursor.execute(sql.format(user.username))
    prefsDog = cursor.fetchall()[0]

    # filtre chat
    sql = "SELECT * FROM preferencesCat WHERE username='{}';"
    cursor.execute(sql.format(user.username))
    prefsCat = cursor.fetchall()[0]

    # filtre oiseau
    sql = "SELECT * FROM preferencesBird WHERE username='{}';"
    cursor.execute(sql.format(user.username))
    prefsBirb = cursor.fetchall()[0]

    for animalId in possible_id:
        sql = "SELECT * from animal WHERE id = '{}';"
        cursor.execute(sql.format(animalId['id']))
        animal = cursor.fetchall()[0]

        if animal['race'] == 'Doggo':
            if prefsDog['maleGenderDoggo'] and animal['sexe'] == 'm' or prefsDog['femaleGenderDoggo'] and animal[
                'sexe'] == 'f':
                if prefsDog['0_20WeightDoggo'] and animal['poids'] <= 20 or prefsDog['20_40WeightDoggo'] and 20 < \
                        animal['poids'] <= 40 or prefsDog['40WeightPlusDoggo'] and animal['poids'] > 40:
                    if prefsDog['0_5AgeDoggo'] and animal['age'] <= 5 or prefsDog['5_10AgeDoggo'] and 5 < animal[
                        'age'] <= 10 or prefsDog['10AgePlusDoggo'] and animal['age'] > 10:
                        sql = "SELECT * FROM dog WHERE id={}"
                        cursor.execute(sql.format(animalId['id']))
                        dog = cursor.fetchall()[0]

                        if prefsDog['declawedDoggo'] == dog['degriffe'] and prefsDog['castratedDoggo'] == dog['castre']:
                            if prefsDog['gingerDoggo'] and dog['pelage'] == 'ginger' or prefsDog['whiteDoggo'] and dog[
                                'pelage'] == 'white' or prefsDog['blackDoggo'] and dog['pelage'] == 'black' or prefsDog[
                                'brownDoggo'] and dog['pelage'] == 'brown' or prefsDog['greyDoggo'] and dog[
                                'pelage'] == 'grey':
                                goodIds.append({'id': animalId['id']})

        elif animal['race'] == 'Kitteh':
            if prefsCat['maleGenderCat'] and animal['sexe'] == 'm' or prefsCat['femaleGenderCat'] and animal[
                'sexe'] == 'f':
                if prefsCat['0_10WeightCat'] and animal['poids'] <= 10 or prefsCat['10_20WeightCat'] and 10 < animal[
                    'poids'] <= 20 or prefsCat['20PlusWeightCat'] and animal['poids'] > 20:
                    if prefsCat['0_5AgeCat'] and animal['age'] <= 5 or prefsCat['5_10AgeCat'] and 5 < animal[
                        'age'] <= 10 or prefsCat['10PlusAgeCat'] and animal['age'] > 10:
                        sql = "SELECT * FROM cat WHERE id={}"
                        cursor.execute(sql.format(animalId['id']))
                        cat = cursor.fetchall()[0]

                        if prefsCat['declawedCat'] == cat['degriffe'] and prefsCat['castratedCat'] == cat['castre']:
                            if prefsCat['gingerCat'] and cat['pelage'] == 'ginger' or prefsCat['whiteCat'] and cat[
                                'pelage'] == 'white' or prefsCat['blackCat'] and cat['pelage'] == 'black' or prefsCat[
                                'brownCat'] and cat['pelage'] == 'brown' or prefsCat['greyCat'] and cat[
                                'pelage'] == 'grey':
                                goodIds.append({'id': animalId['id']})

        elif animal['race'] == 'Birb':
            if prefsBirb['maleBirb'] and animal['sexe'] == 'm' or prefsBirb['femaleBirb'] and animal['sexe'] == 'f':
                if prefsBirb['0_1WeightBirb'] and animal['poids'] <= 1 or prefsBirb['1_2WeightBirb'] and 1 < animal[
                    'poids'] <= 2 or prefsBirb['2PlusWeightBirb'] and animal['poids'] > 3:
                    if prefsBirb['0_5AgeBirb'] and animal['age'] <= 5 or prefsBirb['5_10AgeBirb'] and 5 < animal[
                        'age'] <= 10 or prefsBirb['10AgePlusBirb'] and animal['age'] > 10:
                        sql = "SELECT * FROM bird WHERE id={}"
                        cursor.execute(sql.format(animalId['id']))
                        bird = cursor.fetchall()[0]

                        if prefsBirb['yellowBirb'] and bird['plumage'] == 'yellow' or prefsBirb['blackBirb'] and bird[
                            'plumage'] == 'black' or prefsBirb['whiteBirb'] and bird['plumage'] == 'white' or prefsBirb[
                            'greyBirb'] and bird['plumage'] == 'grey' or prefsBirb['greenBirb'] and bird[
                            'plumage'] == 'green' or prefsBirb['beigeBirb'] and bird['plumage'] == 'beige':
                            goodIds.append({'id': animalId['id']})

    return goodIds


def isYourAnimal(ID, user):
    cursor = get_db()
    cursor.execute("SELECT * FROM vend WHERE username = '{}'".format(user.username))
    animals = cursor.fetchall()
    for animal in animals:
        if str(animal['id_animal']) == str(ID):
            return True
    return False


def get_profile(email):
    cursor = get_db()
    sql = "SELECT * FROM user WHERE email='{}';"
    cursor.execute(sql.format(email))
    result = cursor.fetchall()

    if len(result) != 1:
        return False
    else:
        return result[0]
