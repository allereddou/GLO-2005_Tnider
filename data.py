import pymysql
import uuid
import hashlib
import names
import random

# Code from https://www.pythoncentral.io/hashing-strings-with-python/
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


# new_pass = input('Please enter a password: ')
# hashed_pass = hash_password(new_pass)

db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     db='PROJET_BD')

cursor = db.cursor(pymysql.cursors.DictCursor)

#########################################
# Réinitialisation des bases de données #
#########################################

sql = "DROP TABLE user"
cursor.execute(sql)

sql = "DROP TABLE dog"
cursor.execute(sql)

sql = "DROP TABLE bird"
cursor.execute(sql)

sql = "DROP TABLE cat"
cursor.execute(sql)

sql = "DROP TABLE animal"
cursor.execute(sql)

sql = "CREATE TABLE IF NOT EXISTS user (username VARCHAR(20), pass VARCHAR(100), nom VARCHAR(20), prenom VARCHAR(20), email VARCHAR(40), telephone BIGINT, solde DECIMAL(5,2), PRIMARY KEY (username) );"
cursor.execute(sql)

sql = "CREATE TABLE IF NOT EXISTS animal (id INT PRIMARY KEY , nom VARCHAR(20), sexe CHAR(1), age INT, poids INT, location VARCHAR(20), race VARCHAR(20), description VARCHAR(1000));"
cursor.execute(sql)

sql = "CREATE TABLE IF NOT EXISTS bird(id INT, PRIMARY KEY (id), plumage VARCHAR(20), FOREIGN KEY (id) REFERENCES animal(id) ON DELETE CASCADE);"
cursor.execute(sql)

sql = "CREATE TABLE IF NOT EXISTS dog(id INT, PRIMARY KEY (id), pelage VARCHAR(20), castre BOOLEAN, degriffe BOOLEAN, FOREIGN KEY (id) REFERENCES animal(id) ON DELETE CASCADE);"
cursor.execute(sql)

sql = "CREATE TABLE IF NOT EXISTS cat(id INT, PRIMARY KEY (id), pelage VARCHAR(20), castre BOOLEAN, degriffe BOOLEAN, FOREIGN KEY (id) REFERENCES animal(id) ON DELETE CASCADE);"
cursor.execute(sql)


genders = 'mf'
cities = ['Montreal', 'Quebec', 'Rouyn-Noranda', 'Levis', 'St-Hyacinthe', 'Riviere-Du-Loup', 'London', 'Mongolie Orientale']
races = ['Birb', 'Doggo', 'Kitteh']
plumages = ['blanc', 'noir', 'jaune']
pelages = ['blanc', 'noir', 'brun', 'gris']
binaryChoice = [0, 1]

# Insérer des users
for i in range(0, 101):
    password = random.choice(genders)
    hash = hash_password(password)
    gender = random.choice(genders)
    prenom = names.get_first_name(gender)
    nom = names.get_last_name()
    username = prenom[0:4].lower() + nom[0:4].lower() + str(random.randint(10, 101))
    email = prenom.lower() + nom.lower() + "@hotmail.com"
    telephone = random.randint(1000000000, 10000000000)
    solde = random.randint(0.00, 999.00)

    sql = "INSERT INTO user(username, pass, nom, prenom, email, telephone, solde) VALUES ('{}', '{}', '{}', '{}', '{}', {}, {})"
    cursor.execute(sql.format(username, hash, nom, prenom, email, telephone, solde))

sql = "SELECT * FROM user"
cursor.execute(sql)

for row in cursor:
    print(row)

# Insérer des animaux
for j in range(0, 101):
    sexe = random.choice(genders)
    prenom = names.get_first_name(sexe)
    age = random.randint(0, 11)
    poids = random.randint(0, 101)
    location = random.choice(cities)
    race = random.choice(races)
    description = "Hello there aaaaaaaaaaaaaaaaaa"

    sql = "INSERT INTO animal(id, nom, sexe, age, poids, location, race, description) VALUES ({}, '{}', '{}', {}, {}, '{}', '{}', '{}')"
    cursor.execute(sql.format(j, prenom, sexe, age, poids, location, race, description))

    if race == 'Birb':
        plumage = random.choice(plumages)
        sql = "INSERT INTO bird(id, plumage) VALUES ({},'{}')"
        cursor.execute(sql.format(j, plumage))
    elif race == 'Doggo':
        pelage = random.choice(pelages)
        castre = random.choice(binaryChoice)
        degriffe = random.choice(binaryChoice)
        sql = "INSERT INTO dog(id, pelage, castre, degriffe) VALUES({}, '{}', {}, {})"
        cursor.execute(sql.format(j, pelage, castre, degriffe))
    else:
        pelage = random.choice(pelages)
        castre = random.choice(binaryChoice)
        degriffe = random.choice(binaryChoice)
        sql = "INSERT INTO cat(id, pelage, castre, degriffe) VALUES({}, '{}', {}, {})"
        cursor.execute(sql.format(j, pelage, castre, degriffe))






sql = "SELECT * FROM animal"
cursor.execute(sql)

for row in cursor:
    print(row)
print("\n + \n")



sql = "SELECT * FROM bird"
cursor.execute(sql)

for row in cursor:
    print(row)
print("\n + \n")



sql = "SELECT * FROM dog"
cursor.execute(sql)

for row in cursor:
    print(row)
print("\n + \n")



sql = "SELECT * FROM cat"
cursor.execute(sql)

for row in cursor:
    print(row)
print("\n + \n")
