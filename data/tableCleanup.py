def deleteAllTables(cursor):
    sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'PROJET_BD';"
    tableExists = cursor.execute(sql)

    if tableExists:
        sql = "USE PROJET_BD"
        cursor.execute(sql)

        sql = "DROP TABLE  IF EXISTS dog"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS bird"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS cat"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS vend"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS desire"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS preferencesDog"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS preferencesCat"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS preferencesBird"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS pic"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS notdesired"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS transactions"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS animal"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS user"
        cursor.execute(sql)

        sql = "DROP DATABASE IF EXISTS PROJET_BD"
        cursor.execute(sql)



def createTables(cursor):
    sql = "CREATE DATABASE IF NOT EXISTS PROJET_BD"
    cursor.execute(sql)

    sql = "USE PROJET_BD"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS user (username VARCHAR(20), pass VARCHAR(100), nom VARCHAR(20), prenom VARCHAR(20), email VARCHAR(40), telephone BIGINT, solde DECIMAL(5,2), profileImage VARCHAR(150), PRIMARY KEY (username));"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS animal (id INT PRIMARY KEY , nom VARCHAR(20), sexe CHAR(1), age INT, poids INT, location VARCHAR(20), race VARCHAR(20), description VARCHAR(1000));"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS bird(id INT, PRIMARY KEY (id), plumage VARCHAR(20), sousrace VARCHAR(20), FOREIGN KEY (id) REFERENCES animal(id) ON DELETE CASCADE ON UPDATE CASCADE );"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS dog(id INT, PRIMARY KEY (id), pelage VARCHAR(20), castre TINYINT(1), degriffe TINYINT(1), sousrace VARCHAR(20),  FOREIGN KEY (id) REFERENCES animal(id) ON DELETE CASCADE ON UPDATE CASCADE );"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS cat(id INT, PRIMARY KEY (id), pelage VARCHAR(20), castre TINYINT(1), degriffe TINYINT(1), sousrace VARCHAR(20), FOREIGN KEY (id) REFERENCES animal(id) ON DELETE CASCADE ON UPDATE CASCADE );"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS vend(username VARCHAR(20), id_animal INT, prix DECIMAL(5,2), id_vente INT AUTO_INCREMENT, PRIMARY KEY(id_vente), FOREIGN KEY (username) REFERENCES user(username) ON UPDATE CASCADE, FOREIGN KEY (id_animal) REFERENCES animal(id) ON DELETE CASCADE ON UPDATE CASCADE );"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS pic (id INT NOT NULL, caption VARCHAR(45) NOT NULL, link VARCHAR(200) NOT NULL, PRIMARY KEY(id));"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS desire(username VARCHAR(20), id INT, PRIMARY KEY (username, id), FOREIGN KEY(username) REFERENCES user(username) ON UPDATE CASCADE , FOREIGN KEY(id) REFERENCES animal(id) ON DELETE CASCADE ON UPDATE CASCADE );"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS notdesired(username VARCHAR(20), id INT, PRIMARY KEY (username, id), FOREIGN KEY(username) REFERENCES user(username) ON UPDATE CASCADE , FOREIGN KEY(id) REFERENCES animal(id) ON DELETE CASCADE ON UPDATE CASCADE );"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS preferencesBird(username VARCHAR(20), bird TINYINT(1), blackBirb TINYINT(1), whiteBirb TINYINT(1), blueBirb TINYINT(1), beigeBirb TINYINT(1), greyBirb TINYINT(1), greenBirb TINYINT(1), yellowBirb TINYINT(1), 0_5AgeBirb TINYINT(1), 5_10AgeBirb TINYINT(1), 10AgePlusBirb TINYINT(1), 0_1WeightBirb TINYINT(1), 1_2WeightBirb TINYINT(1), 2PlusWeightBirb TINYINT(1), femaleBirb TINYINT(1), maleBirb TINYINT(1), FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE, PRIMARY KEY(username));"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS preferencesCat(username VARCHAR(20), cat TINYINT(1), declawedCat TINYINT(1), whiteCat TINYINT(1), blackCat TINYINT(1), gingerCat TINYINT(1), greyCat TINYINT(1), brownCat TINYINT(1), castratedCat TINYINT(1),femaleGenderCat TINYINT(1), maleGenderCat TINYINT(1), 0_10WeightCat TINYINT(1), 10_20WeightCat TINYINT(1), 20PlusWeightCat TINYINT(1), 0_5AgeCat TINYINT(1), 5_10AgeCat TINYINT(1), 10PlusAgeCat TINYINT(1), FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE, PRIMARY KEY(username));"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS preferencesDog(username VARCHAR(20), dog TINYINT(1), whiteDoggo TINYINT(1), blackDoggo TINYINT(1), gingerDoggo TINYINT(1), brownDoggo TINYINT(1), greyDoggo TINYINT(1), declawedDoggo TINYINT(1), castratedDoggo TINYINT(1), femaleGenderDoggo TINYINT(1), maleGenderDoggo TINYINT(1), 0_20WeightDoggo TINYINT(1), 20_40WeightDoggo TINYINT(1), 40WeightPlusDoggo TINYINT(1), 0_5AgeDoggo TINYINT(1), 5_10AgeDoggo TINYINT(1), 10AgePlusDoggo TINYINT(1), FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE, PRIMARY KEY(username));"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS transactions(seller VARCHAR(20), id INT, buyer VARCHAR(20), prix DECIMAL(5,2), PRIMARY KEY (seller, id, buyer), FOREIGN KEY(seller) REFERENCES user(username) ON UPDATE CASCADE , FOREIGN KEY(buyer) REFERENCES user(username) ON UPDATE CASCADE , FOREIGN KEY(id) REFERENCES animal(id) ON DELETE CASCADE ON UPDATE CASCADE );"
    cursor.execute(sql)


def createTableIndex(cursor):
    sql = "USE PROJET_BD"
    cursor.execute(sql)

    sql = "CREATE FULLTEXT INDEX userEmail on user(email)"
    cursor.execute(sql)


