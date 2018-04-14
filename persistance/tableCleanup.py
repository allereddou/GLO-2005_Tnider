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

        sql = "DROP TABLE  IF EXISTS cat"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS vend"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS animal"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS preferences"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS user"
        cursor.execute(sql)


        sql = "DROP TABLE IF EXISTS pic"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS desire"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS notdesired"
        cursor.execute(sql)

        sql = "DROP DATABASE IF EXISTS PROJET_BD"
        cursor.execute(sql)



def createTables(cursor):
    sql = "CREATE DATABASE IF NOT EXISTS PROJET_BD"
    cursor.execute(sql)

    sql = "USE PROJET_BD"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS user (username VARCHAR(20), pass VARCHAR(100), nom VARCHAR(20), prenom VARCHAR(20), email VARCHAR(40), telephone BIGINT, solde DECIMAL(5,2), profileImage VARCHAR(150), PRIMARY KEY (username) );"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS animal (id INT PRIMARY KEY , nom VARCHAR(20), sexe CHAR(1), age INT, poids INT, location VARCHAR(20), race VARCHAR(20), description VARCHAR(1000));"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS bird(id INT, PRIMARY KEY (id), plumage VARCHAR(20), FOREIGN KEY (id) REFERENCES animal(id) ON DELETE CASCADE);"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS dog(id INT, PRIMARY KEY (id), pelage VARCHAR(20), castre BOOLEAN, degriffe BOOLEAN, FOREIGN KEY (id) REFERENCES animal(id) ON DELETE CASCADE);"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS cat(id INT, PRIMARY KEY (id), pelage VARCHAR(20), castre BOOLEAN, degriffe BOOLEAN, FOREIGN KEY (id) REFERENCES animal(id) ON DELETE CASCADE);"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS vend(username VARCHAR(20), id_animal INT, id_vente INT AUTO_INCREMENT, prix DECIMAL(5,2), PRIMARY KEY(id_vente), FOREIGN KEY (username) REFERENCES user(username), FOREIGN KEY (id_animal) REFERENCES animal(id) ON DELETE CASCADE);"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS pic (id INT NOT NULL , caption VARCHAR(45) NOT NULL, link VARCHAR(200) NOT NULL, PRIMARY KEY(id));"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS desire(username VARCHAR(20), id INT, PRIMARY KEY (username, id));"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS notdesired(username VARCHAR(20), id INT, PRIMARY KEY (username, id));"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS preferences(username VARCHAR(20), declawedCat TINYINT, whiteCat TINYINT, blackCat TINYINT, gingerCat TINYINT, greyCat TINYINT, brownCat TINYINT, castratedCat TINYINT,femaleGenderCat TINYINT, maleGenderCat TINYINT, 0_10CatWeight TINYINT, 10_20CatWeight TINYINT, 20PlusCatWeight TINYINT, 0_5CatAge TINYINT, 5_10CatAge TINYINT, 10PlusCatAge TINYINT, whiteDoggo TINYINT, blackDoggo TINYINT, gingerDoggo TINYINT, brownDoggo TINYINT, greyDoggo TINYINT, declawedDoggo TINYINT, castratedDoggo TINYINT, femaleGenderDoggo TINYINT, maleGenderDoggo TINYINT, 0_20WeightDoggo TINYINT, 20_40WeightDoggo TINYINT, 40WeightPlusDoggo TINYINT, 0_5AgeDoggo TINYINT, 5_10AgeDoggo TINYINT, 10AgePlusDoggo TINYINT, blackBirb TINYINT, whiteBirb TINYINT, blueBirb TINYINT, beigeBirb TINYINT, greyBirb TINYINT, greenBirb TINYINT, yellowBirb TINYINT, 0_5AgeBirb TINYINT, 5_10AgeBirb TINYINT, 10AgePlusBirb TINYINT, 0_1WeightBirb TINYINT, 1_2WeightBirb TINYINT, 2PlusWeightBirb TINYINT, femaleBirb TINYINT, maleBirb TINYINT, FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE, PRIMARY KEY(username));"
    cursor.execute(sql)
