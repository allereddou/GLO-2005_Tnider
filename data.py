from server import app, get_db
from persistance.tableCleanup import createTables, deleteAllTables, createTableIndex
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
        createTableIndex(cursor)

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







