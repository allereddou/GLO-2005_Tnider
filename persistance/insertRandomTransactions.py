import random


def insertRandomTransactions(cursor):
    sql = "SELECT DISTINCT username FROM user"
    cursor.execute(sql)
    users = cursor.fetchall()

    sql = "SELECT COUNT(*) FROM animal;"
    cursor.execute(sql)
    number_of_animals_in_bd = cursor.fetchall()[0]['COUNT(*)']

    animals = list(range(0, number_of_animals_in_bd))
    random.shuffle(animals)

    present_iterator = 0

    for user in users:
        for i in range(random.randint(0, 2)):
            sql = "INSERT transactions(seller, id, buyer) VALUES('{}', {}, '{}')"
            seller = user['username']
            buyer = chooseRandomBuyer(seller, users)
            animal = animals[present_iterator]
            present_iterator += 1
            cursor.execute(sql.format(seller, animal, buyer))


def chooseRandomBuyer(seller, users):
    buyer = random.choice(users)['username']
    while seller == buyer:
        buyer = random.choice(users)['username']
    return buyer
