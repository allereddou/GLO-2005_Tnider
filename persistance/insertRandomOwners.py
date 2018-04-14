import random

def insertRandomOwners(cursor):
    sql = "SELECT DISTINCT username FROM user"
    cursor.execute(sql)
    users = cursor.fetchall()

    sql = "SELECT COUNT(*) FROM animal;"
    cursor.execute(sql)
    number_of_animals_in_bd = cursor.fetchall()[0]['COUNT(*)']

    sql = "INSERT vend(username, id_animal, prix) VALUES('{}',{},{})"
    cursor.execute(sql.format('admin', 0, random.randint(0, 99)))

    for i in range(1, number_of_animals_in_bd):
        sql = "INSERT vend(username, id_animal, prix) VALUES('{}',{},{})"
        cursor.execute(sql.format(random.choice(users)['username'], i, random.randint(0, 99)))

