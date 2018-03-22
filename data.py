import pymysql
import uuid
import hashlib


# Code from https://www.pythoncentral.io/hashing-strings-with-python/
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


new_pass = input('Please enter a password: ')
hashed_pass = hash_password(new_pass)

db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     db='PROJET_BD')

cursor = db.cursor(pymysql.cursors.DictCursor)

username = 'allereddou'
password = hashed_pass
prenom = "Edouard"
nom = 'Carre'
email = 'edydou4@hotmail.com'
telephone = 8198801040
solde = 500.00


sql = "INSERT INTO user(username, pass, nom, prenom, email, telephone, solde) VALUES ('{}', '{}', '{}', '{}', '{}', {}, {})"


cursor.execute(sql.format(username, password, prenom, nom, email, telephone, solde))

sql = "SELECT * FROM user"
cursor.execute(sql)

for row in cursor:
    print(row)

print("allo %d", 7)
