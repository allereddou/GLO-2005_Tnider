# GLO-2005: Tnider

Dans le cadre du cours GLO-2005: Modèles et langages des bases de données pour ingénieurs, ce TP met en oeuvre les
apprentissages des étudiants de l'équipe. Il consiste en un site Web sur la thématique de notre choix. Vous trouverez
dans le repo tout le rapport et le code nécessaire à la remise. Vous verrez que c'est un ripoff de Tinder, aucuns droits ne sont réservés et tout a été fait dans un but d'apprentissage dans le cadre du cours qui recommendait de s'inspirer de sites connus. 

## Prérequis

* [python v3.6.x](https://www.python.org/downloads/)
* [pip v9.0.x](https://pypi.python.org/pypi/pip)
* [mySQL](https://www.mysql.com/downloads/)

Ces packages sont nécessaires pour rouler l'application. Il faut tout d'abord les installer, puis il sera possible de 
démarrer l'application.

## Installation

```
pip install -r requirements.txt
```

## Démarrage

Il faut tout d'abord s'assurer que mySQL est en opération sur le système, puis l'on peut continuer
avec ces étapes si mySQL fonctionne. Aussi, certaines fonctionnalités doivent communiquer avec Internet, pour que 
jQuery fonctionne entre autres, donc une connexion Internet fonctionnelle est requise.

### MySQL informations par défault

```
host='localhost',
port=3306,
user='root',
autocommit=True
```

### Générer de l'information
Par défaut, 1000 animaux et 102 users sont générés. Pour les générer, il faut rouler le fichier ```data.py```.
```
python3 data.py
```

## Rouler l'application

#### Mac

```
python3 server.py
```

#### Linux

```
python3 server.py
```

Ensuite, on peut accéder à la page via ```localhost:5000```.

Un utilisateur admin est offert pour tester avec comme email ```admin@hotmail.com``` et comme mot de passe, ```admin```.

## Contributeurs

* [Olivier Gamache](https://github.com/olgam4)
* [Édouard Carré](https://github.com/allereddou)
* Sébastien Paquet

### Remerciements

* Ph.D Richard Khoury

## Ont été utilisés

* [MaterializeCSS](http://www.materializecss.com)
* [fontAwesome](https://fontawesome.com)
* [StackOverflow](https://stackoverflow.com)
