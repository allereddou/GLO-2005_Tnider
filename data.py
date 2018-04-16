from server import app, get_db
from persistance.tableCleanup import createTables, deleteAllTables
from persistance.insertRandomUsers import insertUsers
from persistance.insertRandomAnimals import insertAnimal
from persistance.imageLinks import insertBirbPics, insertDoggoPics, insertKittehPics
from persistance.insertRandomDesired import insertRandomDesired
from persistance.insertRandomTransactions import insertRandomTransactions
from persistance.insertRandomOwners import insertRandomOwners


def setupDatabase():
    with app.app_context():
        # ouverture connexion
        cursor = get_db()

        # supprimer les tables
        deleteAllTables(cursor)
        createTables(cursor)

        # insérer des users
        insertUsers(cursor, 100)

        # insérer des animaux
        insertAnimal(cursor, 1000)

        # insérer des photos d'oiseaux
        insertBirbPics(cursor)

        # insérer des photos de doggo
        insertDoggoPics(cursor)

        # insérer des photos de chats
        insertKittehPics(cursor)

        # insérer des transactions
        insertRandomTransactions(cursor)

        # insérer des owners
        insertRandomOwners(cursor)

        # insérer des wishlits
        insertRandomDesired(cursor)


with app.app_context():
    setupDatabase()

    sql = "SELECT * FROM user"
    cursor = get_db()

    cursor.execute(sql)

    sql = "INSERT INTO  preferencesDog(username, whiteDoggo, blackDoggo, gingerDoggo, brownDoggo, greyDoggo, declawedDoggo, castratedDoggo, femaleGenderDoggo, maleGenderDoggo, 0_20WeightDoggo, 20_40WeightDoggo, 40WeightPlusDoggo, 0_5AgeDoggo, 5_10AgeDoggo, 10AgePlusDoggo) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
    cursor.execute(sql.format('admin'))

    sql = "INSERT INTO preferencesBird(username, blackBirb, whiteBirb, blueBirb, beigeBirb, greyBirb, greenBirb, yellowBirb, 0_5AgeBirb, 5_10AgeBirb, 10AgePlusBirb, 0_1WeightBirb, 1_2WeightBirb, 2PlusWeightBirb, femaleBirb, maleBirb) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
    cursor.execute(sql.format('admin'))

    sql = "INSERT INTO preferencesCat(username, declawedCat, whiteCat, blackCat, gingerCat, greyCat, brownCat, castratedCat,femaleGenderCat, maleGenderCat, 0_10WeightCat, 10_20WeightCat, 20PlusWeightCat, 0_5AgeCat, 5_10AgeCat, 10PlusAgeCat) VALUES ('{}', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);"
    cursor.execute(sql.format('admin'))




