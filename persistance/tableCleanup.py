def deleteAllTables(cursor):
    sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'PROJET_BD';"
    tableExists = cursor.execute(sql)

    if (tableExists == 1):
        sql = "USE IF EXISTS PROJET_BD"
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

        sql = "DROP TABLE IF EXISTS user"
        cursor.execute(sql)

        sql = "DROP TABLE IF EXISTS pic"
        cursor.execute(sql)

        sql = "DROP DATABASE IF EXISTS PROJET_BD"
        cursor.execute(sql)


def createTables(cursor):
    sql = "CREATE DATABASE IF NOT EXISTS PROJET_BD"
    cursor.execute(sql)

    sql = "USE PROJET_BD"
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

    sql = "CREATE TABLE IF NOT EXISTS vend(username VARCHAR(20), id_animal INT, id_vente INT AUTO_INCREMENT, PRIMARY KEY(id_vente), FOREIGN KEY (username) REFERENCES user(username), FOREIGN KEY (id_animal) REFERENCES animal(id) ON DELETE CASCADE);"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS pic (idpic INTEGER UNSIGNED NOT NULL , caption VARCHAR(45) NOT NULL, img LONGBLOB NOT NULL, PRIMARY KEY(idpic));"
    cursor.execute(sql)
