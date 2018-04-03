import pymysql
from persistance.tableCleanup import createTables, deleteAllTables
from persistance.insertRandomUsers import insertUsers
from persistance.insertRandomAnimals import insertAnimal






# Ouverture de la connexion
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root')

cursor = db.cursor(pymysql.cursors.DictCursor)

#########################################
# Réinitialisation des bases de données #
#########################################
deleteAllTables(cursor)
createTables(cursor)

# Insérer des users
insertUsers(cursor, 100)

sql = "SELECT * FROM user"
cursor.execute(sql)

for row in cursor:
    print(row)

# Insérer des animaux
insertAnimal(cursor, 100)

sql = "SELECT * FROM animal"
cursor.execute(sql)

for row in cursor:
    print(row)
print(2 * "\n")

sql = "SELECT * FROM bird"
cursor.execute(sql)

for row in cursor:
    print(row)
print(2 * "\n")

sql = "SELECT * FROM dog"
cursor.execute(sql)

for row in cursor:
    print(row)
print(2 * "\n")

sql = "SELECT * FROM cat"
cursor.execute(sql)

for row in cursor:
    print(row)
print(2 * "\n")



