from persistance.passwordUtil import hash_password
import names
import random

genders = 'mf'

defaultProfileImage = "https://accrualnet.cancer.gov/sites/accrualnet.cancer.gov/themes/accrualnet/accrualnet-internals/images/avatars/male/Red.png"


def insertUsers(cursor, number):
    for i in range(0, number + 1):
        password = random.choice(genders)
        hashed = hash_password(password)
        gender = random.choice(genders)
        prenom = names.get_first_name(gender)
        nom = names.get_last_name()
        username = prenom[0:4].lower() + nom[0:4].lower() + str(random.randint(10, 101))
        email = prenom.lower() + nom.lower() + "@hotmail.com"
        telephone = random.randint(1000000000, 10000000000)
        solde = random.randint(0.00, 999.00)

        sql = "INSERT INTO user(username, pass, nom, prenom, email, telephone, solde, profileImage) VALUES ('{}', '{}', '{}', '{}', '{}', {}, {}, '{}')"
        cursor.execute(sql.format(username, hashed, nom, prenom, email, telephone, solde, defaultProfileImage))

        username = "admin"
        password = "admin"
        hashed = hash_password(password)
        nom = "admin"
        prenom = "admin"
        email = "admin@hotmail.com"
        telephone = random.randint(1000000000, 10000000000)
        solde = 0.0

        if i == 0:
            sql = "INSERT INTO user(username, pass, nom, prenom, email, telephone, solde, profileImage) VALUES ('{}', '{}', '{}', '{}', '{}', {}, {}, '{}')"
            cursor.execute(sql.format(username, hashed, nom, prenom, email, telephone, solde, defaultProfileImage))




