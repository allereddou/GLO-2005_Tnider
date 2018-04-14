import random

def insertRandomDesired(cursor):
    sql = "SELECT A.id FROM animal A WHERE A.id not in (SELECT id FROM transactions);"
    cursor.execute(sql)
    animal_ids = cursor.fetchall()
    sql = "SELECT * FROM user;"
    cursor.execute(sql)
    users = cursor.fetchall()
    for user in users:
        possibilities = list()
        for id in animal_ids:
            possibilities.append(id['id'])
        random.shuffle(possibilities)
        for i in range(random.randint(0, 15)):
            sql = "SELECT username, id_animal FROM vend WHERE username = '{}'".format(user['username'])
            cursor.execute(sql)
            animals = cursor.fetchall()
            current_id = possibilities.pop()
            for animal in animals:
                if animal['id_animal'] == current_id:
                    continue
            sql = "INSERT desire(username, id) VALUES ('{}', {});"
            cursor.execute(sql.format(user['username'], current_id))
