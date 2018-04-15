from datetime import timedelta
import pymysql
from flask import Flask, render_template, request, g, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import random

from Forms.LoginForm import LoginForm, RegisterForm
from Users import *
from persistance.bdUtils import createUser, checkIfUsernameAlreadyUsed, checkIfEmailAlreadyUsed, validatePassword, \
    updatePreferences
from persistance.passwordUtil import hash_password

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY="plz giv boop and nuggers",
    REMEMBER_COOKIE_DURATION=timedelta(days=7)
))

login_manager = LoginManager()
login_serializer = URLSafeTimedSerializer(app.secret_key)

defaultProfileImage = "https://accrualnet.cancer.gov/sites/accrualnet.cancer.gov/themes/accrualnet/accrualnet-internals/images/avatars/male/Red.png"


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/account/myanimals')
@login_required
def myanimals():
    cursor = get_db()
    cursor.execute(
        "SELECT P.link, A.nom, A.id FROM vend V, animal A, pic P WHERE V.username = '{}' and V.id_animal = A.id and P.id = A.id".format(current_user.username))
    tosell = cursor.fetchall()
    return render_template('account-my-animals.html', tosell=tosell)


@app.route('/account/trash/<num>')
def trash(num):
    cursor = get_db()
    cursor.execute("DELETE FROM animal WHERE id = {}".format(num))
    return redirect(request.referrer)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/browse', methods=['GET', 'POST'])
@login_required
def browse():
    global dispo
    wishlist = get_animals_desired()
    dispo = get_possible_match()
    if request.method == 'GET':
        return render_template('browse.html', wishlist=wishlist, animal=dispo, first=dispo['id'])
    if request.method == 'POST':
        return render_template('browse.html', wishlist=wishlist, dispo=wishlist, first=first)


@app.route('/browse/like')
@login_required
def like():
    cursor = get_db()
    cursor.execute("INSERT desire(username, id) VALUES ('{}', {})".format(current_user.username, dispo['id']))
    return redirect(request.referrer)


@app.route('/browse/dislike')
@login_required
def dislike():
    cursor = get_db()
    cursor.execute("INSERT notdesired(username, id) VALUES ('{}', {})".format(current_user.username, dispo['id']))
    return redirect(request.referrer)


@app.route('/deletenotdesired')
@login_required
def delete_not_desired():
    cursor = get_db()
    cursor.execute("DELETE FROM notdesired WHERE username = '{}'".format(current_user.username))
    return redirect(request.referrer)


@app.route('/browse/delete')
@login_required
def delete_desired():
    num = request.args['num']
    cursor = get_db()
    cursor.execute(
        "DELETE FROM desire WHERE username = '{}' and id = {}".format(current_user.username, num))
    return redirect(request.referrer)


@app.route('/browse/buy')
@login_required
def buy():
    num = request.args['num']
    cursor = get_db()
    cursor.execute("SELECT * FROM vend WHERE id_animal = {}".format(num))
    vend = cursor.fetchall()[0]
    current_user.solde -= vend['prix']
    cursor.execute("UPDATE user SET solde = {} WHERE username = '{}'".format(current_user.solde, current_user.username))
    cursor.execute(
        "INSERT transactions(seller, id, buyer, prix) VALUES('{}',{},'{}',{})".format(vend['username'], num,
                                                                                      current_user.username,
                                                                                      vend['prix']))
    cursor.execute("DELETE FROM desire WHERE id = {}".format(num))
    cursor.execute("DELETE FROM notdesired WHERE id = {}".format(num))
    cursor.execute("DELETE FROM vend WHERE id_animal = {}".format(num))
    return redirect(request.referrer)


@app.route('/account')
@login_required
def sign_in():
    return render_template('account.html')


@app.route('/contact_us')
def contact_us():
    print(current_user.preferences)
    return render_template('contact_us.html')


@app.route('/account/preferences', methods=["GET", "POST"])
@login_required
def account_preferences():
    if request.method == "GET" and request.args.to_dict().get('Save') == "Save":
        current_user.preferences = updatePreferences(current_user, request.args.to_dict())
    return render_template("account-preferences.html", pref=current_user.preferencesCat.keys())


@app.route('/account/transactions')
@login_required
def account_transactions():
    cursor = get_db()
    cursor.execute(
        "SELECT T.buyer, T.seller, A.nom FROM transactions T, animal A WHERE T.seller = '{}' and A.id = T.id".format(
            current_user.username))
    sold = cursor.fetchall()

    cursor = get_db()
    cursor.execute(
        "SELECT T.buyer, T.seller, A.nom FROM transactions T, animal A WHERE T.buyer = '{}' and A.id = T.id".format(
            current_user.username))
    bought = cursor.fetchall()

    return render_template('account-transactions.html', sold=sold, bought=bought)


@app.route('/account/info')
@login_required
def account_info():
    return render_template('account-info.html')


@app.route('/account/info/change/<field>=<new>')
@login_required
def change(field, new):
    cursor = get_db()
    if field == 'telephone' and isinstance(new, int):
        cursor.execute("UPDATE user SET {} = {} WHERE username = '{}'".format(field, new, current_user.username))
    elif field == 'pass':
        new = hash_password(new)
        cursor.execute("UPDATE user SET {} = '{}' WHERE username = '{}'".format(field, new, current_user.username))
    else:
        cursor.execute("UPDATE user SET {} = '{}' WHERE username = '{}'".format(field, new, current_user.username))
    return redirect(request.referrer)


@app.route('/account/info/change/image/<field>=<path:new>')
@login_required
def changeimg(field, new):
    cursor = get_db()
    cursor.execute("UPDATE user SET {} = '{}' WHERE username = '{}'".format(field, new, current_user.username))
    return redirect(request.referrer)


@app.route('/user/<username>')
@login_required
def username(username):
    cursor = get_db()
    cursor.execute("SELECT U.username, U.nom, U.prenom, U.nom, U.email, U.profileImage, U.telephone FROM user U WHERE U.username = '{}'".format(username))
    user = cursor.fetchall()[0]
    return render_template('user.html', user=user)


@app.route('/addAnimal')
@login_required
def add_Animal():
    return render_template('addAnimals.html')


@app.route("/", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("browse"))
    login_form = LoginForm(request.form)
    register_form = RegisterForm(request.form)

    if request.method == "POST":
        if login_form.validate_on_submit() and request.form['btn'] == "Login":
            user = User.get(login_form.email.data)

            if user and validatePassword(login_form.email.data, login_form.password.data):
                login_user(user, remember=True)

                return redirect(request.args.get("next") or url_for("browse"))

        if register_form.validate_on_submit() and request.form['btn'] == "Create":
            if not checkIfUsernameAlreadyUsed(register_form.username.data):
                print("username not valid !")
                return render_template("home.html")

            if not checkIfEmailAlreadyUsed(register_form.email.data):
                print("email not valid !")
                return render_template("home.html")

            user = User(register_form.email.data, register_form.password2.data, register_form.username.data,
                        register_form.last_name.data, register_form.first_name.data, register_form.phone_number.data, 0,
                        defaultProfileImage)

            createUser(user)
            login_user(user, remember=True)
            return redirect(request.args.get("next") or url_for("browse"))

    return render_template("home.html")


@app.route("/logout/")
def logout_page():
    logout_user()
    return redirect("/")


def get_db():
    sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'PROJET_BD';"

    if not hasattr(g, 'cursor'):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             autocommit=True)

        g.cursor = db.cursor(pymysql.cursors.DictCursor)
        schemaExists = g.cursor.execute(sql)

        if not schemaExists:
            sql = "CREATE DATABASE IF NOT EXISTS PROJET_BD"
            g.cursor.execute(sql)

        g.cursor.execute("USE PROJET_BD")
    return g.cursor


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'cursor'):
        g.cursor.close()


@login_manager.user_loader
def load_user(email):
    return User.get(email)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("home")


def get_animals_desired():
    cursor = get_db()
    cursor.execute("SELECT D.id FROM desire D WHERE D.username = '{}'".format(current_user.username))
    id_wishlist = cursor.fetchall()
    wishlist = []
    for current_id in id_wishlist:
        cursor.execute(
            "SELECT DISTINCT A.id, P.link, A.sexe, A.age, A.poids, A.description, A.nom, A.race, A.location, V.username, V.prix FROM pic P, animal A, vend V WHERE A.id = V.id_animal and A.id = P.id and A.id = {};".format(
                current_id['id']))
        animal = cursor.fetchall()[0]
        if animal['race'] == 'Kitteh':
            cursor.execute("SELECT pelage, castre, degriffe FROM cat WHERE id = {}".format(animal['id']))
        elif animal['race'] == 'Doggo':
            cursor.execute("SELECT pelage, castre, degriffe FROM dog WHERE id = {}".format(animal['id']))
        elif animal['race'] == 'Birb':
            cursor.execute("SELECT plumage FROM bird WHERE id = {}".format(animal['id']))
        race = cursor.fetchall()[0]
        wishlist.append({**animal, **race})
    return wishlist


def get_profile(email):
    cursor = get_db()
    sql = "SELECT * FROM user WHERE email='{}';"
    cursor.execute(sql.format(email))
    result = cursor.fetchall()

    if len(result) != 1:
        return False
    else:
        return result[0]


# cette fonction doit être modifiée pour trouver un animal
def get_possible_match():
    cursor = get_db()
    sql = "SELECT A.id FROM animal A WHERE A.id not in (SELECT D.id FROM desire D WHERE D.username = '{}') and A.id not in (SELECT D.id FROM notdesired D WHERE D.username = '{}') and A.id not in (SELECT T.id FROM transactions T) and A.id not in (SELECT V.id_animal FROM vend V WHERE V.username = '{}');".format(
        current_user.username, current_user.username, current_user.username)
    cursor.execute(sql)
    possible_id = cursor.fetchall()

    print(possible_id)

    filterIds(possible_id)

    IDs = list()
    for i in possible_id:
        IDs.append(i['id'])
    random.shuffle(IDs)
    sql = "SELECT DISTINCT A.id, P.link, A.nom, A.race, A.location, A.sexe, A.age, A.poids, A.description FROM pic P, animal A WHERE A.id = P.id and A.id = {}".format(
        IDs.pop())
    cursor.execute(sql)
    animal = cursor.fetchall()[0]
    if animal['race'] == 'Kitteh':
        cursor.execute("SELECT pelage, castre, degriffe FROM cat WHERE id = {}".format(animal['id']))
    elif animal['race'] == 'Doggo':
        cursor.execute("SELECT pelage, castre, degriffe FROM dog WHERE id = {}".format(animal['id']))
    elif animal['race'] == 'Birb':
        cursor.execute("SELECT plumage FROM bird WHERE id = {}".format(animal['id']))
    race = cursor.fetchall()[0]
    cursor.execute("SELECT prix FROM vend WHERE id_animal = {}".format(animal['id']))
    prix = cursor.fetchall()[0]
    return {**animal, **race, **prix}


def filterIds(possible_id):
    cursor = get_db()
    goodIds = []


    # filtre chien
    sql = "SELECT * FROM preferencesDog WHERE username='{}';"
    cursor.execute(sql.format(current_user.username))
    prefsDog = cursor.fetchall()[0]

    # filtre chat
    sql = "SELECT * FROM preferencesCat WHERE username='{}';"
    cursor.execute(sql.format(current_user.username))
    prefsCat = cursor.fetchall()[0]

    # filtre oiseau
    sql = "SELECT * FROM preferencesBird WHERE username='{}';"
    cursor.execute(sql.format(current_user.username))
    prefsBirb = cursor.fetchall()[0]

    for animalId in possible_id:
        sql = "SELECT * from animal WHERE id = '{}';"
        cursor.execute(sql.format(animalId['id']))
        animal = cursor.fetchall()[0]

        if prefsDog['maleGenderDoggo'] == 1 and animal['sexe'] == 'm' or prefsDog['femaleGenderDoggo'] == 1 and animal['sexe'] == 'f':
            if prefsDog['0_20WeigthDoggo'] == 1 and animal['poids'] <= 20 or prefsDog['20_40Weight'] == 1 and 20 < animal['poids'] < 40 or prefsDog['40WeigthPlusDoggo'] == 1 and animal['poids'] > 40:
                if prefsDog['0_5AgeDoggo'] == 1 and animal['age'] <= 5 or prefsDog['5_10AgeDoggo'] == 1 and 5 < animal['age'] <= 10 or prefsDog['10AgePlusDoggo'] == 1 and animal['age'] > 10:
                    sql = "SELECT * FROM dog WHERE id={}"
                    cursor.execute(sql.format(animalId))
                    dog = cursor.fetchall()[0]

                    if prefsDog['declawedDoggo'] == dog['degriffe'] and prefsDog['castratedDoggo'] == dog['castre']:
                        if prefsDog['gingerDoggo'] == 1 and dog['pelage'] == 'roux' or prefsDog['whiteDoggo'] == 1 and dog['pelage'] == 'blanc' or prefsDog['blackDoggo'] and dog['pelage'] == 'noir' or prefsDog['brownDoggo'] == 1 and dog['pelage'] == 'brun' or prefsDog['greyDoggo'] == 1 and dog['pelage'] == 'gris':
                            goodIds.append(animalId)

        elif prefsCat['maleGenderCat'] == 1 and animal['sexe'] == 'm' or prefsCat['femaleGenderDoggo'] == 1 and animal['sexe'] == 'f':
            if prefsCat['0_10WeigthCat'] == 1 and animal['poids'] <= 10 or prefsCat['10_20Weight'] == 1 and 10 < animal['poids'] <= 20 or prefsCat['20WeigthPlusCat'] == 1 and animal['poids'] > 20:
                if prefsCat['0_5AgeCat'] == 1 and animal['age'] <= 5 or prefsCat['5_10AgeCat'] == 1 and 5 < animal['age'] <= 10 or prefsCat['10AgePlusCat'] == 1 and animal['age'] > 10:
                    sql = "SELECT * FROM cat WHERE id={}"
                    cursor.execute(sql.format(animalId))
                    cat = cursor.fetchall()[0]

                    if prefsCat['declawedCat'] == cat['degriffe'] and prefsCat['castratedCat'] == cat['castre']:
                        if prefsCat['gingerCat'] == 1 and cat['pelage'] == 'roux' or prefsCat['whiteCat'] == 1 and cat['pelage'] == 'blanc' or prefsCat['blackCat'] and cat['pelage'] == 'noir' or prefsCat['brownCat'] == 1 and cat['pelage'] == 'brun' or prefsCat['greyCat'] == 1 and cat['pelage'] == 'gris':
                            goodIds.append(animalId)

        defaultPrefBird = {'blackBirb': 1, 'greenBirb': 1, '1_2WeightBirb': 1, 'maleBirb': 1, 'greyBirb': 1,
                           '10AgePlusBirb': 1,
                           'whiteBirb': 1, 'blueBirb': 1, '0_1WeightBirb': 1, '2PlusWeightBirb': 1, 'yellowBirb': 1,
                           '5_10AgeBirb': 1, 'femaleBirb': 1, 'beigeBirb': 1, '0_5AgeBirb': 1}


        elif prefsBirb['maleGenderBirb'] == 1 and animal['sexe'] == 'm' or prefsBirb['femaleGenderBirb'] == 1 and animal['sexe'] == 'f':
            if prefsBirb['0_1WeigthBirb'] == 1 and animal['poids'] <= 1 or prefsBirb['1_2Weight'] == 1 and 1 < animal['poids'] <= 2 or prefsBirb['2PlusWeigthBirb'] == 1 and animal['poids'] > 3:
                if prefsBirb['0_5AgeBirb'] == 1 and animal['age'] <= 5 or prefsBirb['5_10AgeBirb'] == 1 and 5 < animal['age'] <= 10 or prefsBirb['10AgePlusBirb'] == 1 and animal['age'] > 10:
                    sql = "SELECT * FROM bird WHERE id={}"
                    cursor.execute(sql.format(animalId))
                    bird = cursor.fetchall()[0]

                    if prefsBirb['yellowBirb'] == 1 and bird['plumage'] == 'yellow' or prefsBirb['blackBirb'] == 1 and bird['plumage'] == 'black' or prefsBirb['whiteBirb'] and bird['plumage'] == 'white' or prefsBirb['brownCat'] == 1 and bird['plumage'] == 'brun' or prefsBirb['greyCat'] == 1 and bird['plumage'] == 'gris':
                        goodIds.append(animalId)



                plumages = ['blanc', '', '', 'gris', 'beige', 'vert']




if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(debug=True)
