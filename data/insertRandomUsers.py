from persistance.passwordUtil import hash_password
import names
import random

genders = 'mf'

defaultProfileImage = "https://accrualnet.cancer.gov/sites/accrualnet.cancer.gov/themes/accrualnet/accrualnet-internals/images/avatars/male/Red.png"


def insertUsers(cursor, number):
    for i in range(0, number + 1):
        if i > 0:
            password = random.choice(genders)
            hashed = hash_password(password)
            gender = random.choice(genders)
            prenom = names.get_first_name(gender)
            nom = names.get_last_name()
            username = prenom[0:4].lower() + nom[0:4].lower() + str(random.randint(10, 101))
            email = prenom.lower() + nom.lower() + "@hotmail.com"
            telephone = random.randint(1000000000, 10000000000)
            solde = random.randint(0.00, 999.00)
            try:
                sql = "INSERT INTO user(username, pass, nom, prenom, email, telephone, solde, profileImage) VALUES ('{}', '{}', '{}', '{}', '{}', {}, {}, '{}')"
                cursor.execute(sql.format(username, hashed, nom, prenom, email, telephone, solde, defaultProfileImage))

                sql = "INSERT INTO  preferencesDog(username, dog, whiteDoggo, blackDoggo, gingerDoggo, brownDoggo, greyDoggo, declawedDoggo, castratedDoggo, femaleGenderDoggo, maleGenderDoggo, 0_20WeightDoggo, 20_40WeightDoggo, 40WeightPlusDoggo, 0_5AgeDoggo, 5_10AgeDoggo, 10AgePlusDoggo) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
                cursor.execute(sql.format(username))

                sql = "INSERT INTO preferencesBird(username, bird, blackBirb, whiteBirb, blueBirb, beigeBirb, greyBirb, greenBirb, yellowBirb, 0_5AgeBirb, 5_10AgeBirb, 10AgePlusBirb, 0_1WeightBirb, 1_2WeightBirb, 2PlusWeightBirb, femaleBirb, maleBirb) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
                cursor.execute(sql.format(username))

                sql = "INSERT INTO preferencesCat(username, cat, declawedCat, whiteCat, blackCat, gingerCat, greyCat, brownCat, castratedCat,femaleGenderCat, maleGenderCat, 0_10WeightCat, 10_20WeightCat, 20PlusWeightCat, 0_5AgeCat, 5_10AgeCat, 10PlusAgeCat) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
                cursor.execute(sql.format(username))
            except:
                continue

        if i == 0:
            username = "admin"
            password = "admin"
            hashed = hash_password(password)
            nom = "admin"
            prenom = "admin"
            email = "admin@hotmail.com"
            telephone = random.randint(1000000000, 10000000000)
            solde = random.randint(0, 999)
            sql = "INSERT INTO user(username, pass, nom, prenom, email, telephone, solde, profileImage) VALUES ('{}', '{}', '{}', '{}', '{}', {}, {}, '{}')"
            cursor.execute(sql.format(username, hashed, nom, prenom, email, telephone, solde, defaultProfileImage))

            sql = "INSERT INTO  preferencesDog(username, dog, whiteDoggo, blackDoggo, gingerDoggo, brownDoggo, greyDoggo, declawedDoggo, castratedDoggo, femaleGenderDoggo, maleGenderDoggo, 0_20WeightDoggo, 20_40WeightDoggo, 40WeightPlusDoggo, 0_5AgeDoggo, 5_10AgeDoggo, 10AgePlusDoggo) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
            cursor.execute(sql.format('admin'))

            sql = "INSERT INTO preferencesBird(username, bird, blackBirb, whiteBirb, blueBirb, beigeBirb, greyBirb, greenBirb, yellowBirb, 0_5AgeBirb, 5_10AgeBirb, 10AgePlusBirb, 0_1WeightBirb, 1_2WeightBirb, 2PlusWeightBirb, femaleBirb, maleBirb) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
            cursor.execute(sql.format('admin'))

            sql = "INSERT INTO preferencesCat(username, cat, declawedCat, whiteCat, blackCat, gingerCat, greyCat, brownCat, castratedCat,femaleGenderCat, maleGenderCat, 0_10WeightCat, 10_20WeightCat, 20PlusWeightCat, 0_5AgeCat, 5_10AgeCat, 10PlusAgeCat) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
            cursor.execute(sql.format('admin'))




