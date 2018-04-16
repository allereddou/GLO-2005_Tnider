# GLO-2005: Tnider

Dans le cadre du cours GLO-2005: Modèles et langages des bases de données pour ingénieurs, ce TP met en oeuvre les
apprentissages des étudiants de l'équipe. Il consiste en un site Web sur la thématique de notre choix. Vous trouverez
dans le repo tout le rapport et le code nécessaire à la remise.

## Prérequis

* [python v3.6.x](https://www.python.org/downloads/)
* [pip v9.0.x](https://pypi.python.org/pypi/pip)
* [mySQL](https://www.mysql.com/downloads/)

Ces packages sont nécessaires pour rouler l'application. Il faut tout d'abord les installer, puis il sera possible de 
démarrer l'application.

## Installation

```
pip install -r requirements.txt
python3 data.py
```

## Démarrage

Il faut tout d'abord s'assurer que mySQL est en opération sur le système avant toute chose, puis l'on peut continuer
avec ces étapes si mySQL fonctionne.

### Mac

```
export FLASK_APP={YOUR_PATH_TO_THE_server.py}  
flask run --port={port}  
```

### Linux

```
export FLASK_APP={YOUR_PATH_TO_THE_server.py}  
flask run --port={port}
```

## Contributeurs

* Olivier Gamache
* Édouard Carré
* Sébastien Paquet

### Remerciements

* Ph.D Richard Khoury

## Ont été utilisés

* [MaterializeCSS](http://www.materializecss.com)
* [fontAwesome](https://fontawesome.com)
* [StackOverflow](https://stackoverflow.com)
