import random

def insertRandomDesired(cursor):
    sql = "SELECT COUNT(*) FROM animal;"
    cursor.execute(sql)
    number_of_animals_in_bd = cursor.fetchall()[0]['COUNT(*)']
    sql = "SELECT * FROM user U;"
    cursor.execute(sql)
    users = cursor.fetchall()
    for user in users:
        possibilites = list(range(number_of_animals_in_bd))
        random.shuffle(possibilites)
        for i in range(random.randint(0, 5)):
            sql = "INSERT desire(username, id) VALUES ('{}', {});"
            current_id = possibilites.pop()
            cursor.execute(sql.format(user['username'], current_id))


