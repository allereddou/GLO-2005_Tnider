import random

def insertRandomDesired(cursor):
    sql = "SELECT id FROM animal WHERE id not in (SELECT id FROM transactions);"
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
            sql = "INSERT desire(username, id) VALUES ('{}', {});"
            current_id = possibilities.pop()
            cursor.execute(sql.format(user['username'], current_id))


