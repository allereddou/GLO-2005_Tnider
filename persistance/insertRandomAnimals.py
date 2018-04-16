import random
import names

races = ['Birb', 'Doggo', 'Kitteh']
plumages = ['white', 'black', 'yellow', 'grey', 'beige', 'green']
pelages = ['white', 'black', 'brown', 'grey', 'ginger']
binaryChoice = [0, 1]
genders = 'mf'
cities = ['Montreal', 'Quebec', 'Rouyn-Noranda', 'Levis', 'St-Hyacinthe', 'Riviere-Du-Loup', 'London',
          'Mongolie Orientale']
descriptions = ['reeeeeeeeeeeee', 'aaaaaaaaaaa', 'Hello there', 'Boop', 'l ll ll l_', 's+e', 'o+e', 'Hello doug',
                'No this is patrick', 'Shrek is love, Shrek is life', 'boop boop', 'bork bork', 'plz boop me',
                'floof', 'zoooop']

sousraceChat = ['minou', 'beuglant', 'gros']
sousraceChien = ['bulldog', 'groschien', 'grrr']
sousraceBirb = ['cute', 'wow']


def insertAnimal(cursor, number):
    for j in range(0, number + 1):
        sexe = random.choice(genders)
        if sexe == 'f':
            prenom = names.get_first_name(gender='female')
        else:
            prenom = names.get_first_name(gender='male')

        age = random.randint(0, 15)
        location = random.choice(cities)
        race = random.choice(races)

        if race == 'Birb':
            poids = random.randint(0, 10)
        elif race == 'Cat':
            poids = random.randint(0, 30)
        else:
            poids = random.randint(0, 50)
        description = random.choice(descriptions)

        sql = "INSERT INTO animal(id, nom, sexe, age, poids, location, race, description) VALUES ({}, '{}', '{}', {}, {}, '{}', '{}', '{}')"
        cursor.execute(sql.format(j, prenom, sexe, age, poids, location, race, description))

        # insert in the animal in corresponding database
        if race == 'Birb':
            plumage = random.choice(plumages)
            sousrace = random.choice(sousraceBirb)
            sql = "INSERT INTO bird(id, plumage, sousrace) VALUES ({},'{}', '{}')"
            cursor.execute(sql.format(j, plumage, sousrace))
        elif race == 'Doggo':
            pelage = random.choice(pelages)
            castre = random.choice(binaryChoice)
            degriffe = random.choice(binaryChoice)
            sousrace = random.choice(sousraceChien)
            sql = "INSERT INTO dog(id, pelage, castre, degriffe, sousrace) VALUES({}, '{}', {}, {}, '{}')"
            cursor.execute(sql.format(j, pelage, castre, degriffe, sousrace))
        else:
            pelage = random.choice(pelages)
            castre = random.choice(binaryChoice)
            degriffe = random.choice(binaryChoice)
            sousrace = random.choice(sousraceChat)
            sql = "INSERT INTO cat(id, pelage, castre, degriffe, sousrace) VALUES({}, '{}', {}, {},'{}')"
            cursor.execute(sql.format(j, pelage, castre, degriffe, sousrace))
