from datetime import timedelta
import pymysql
from flask import Flask, render_template, request, g, redirect, url_for
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
        "SELECT P.link, A.nom, A.id, A.race, A.sexe, A.poids, A.age, V.prix, A.location, A.description FROM vend V, animal A, pic P WHERE V.username = '{}' and V.id_animal = A.id and P.id = A.id".format(
            current_user.username))
    tosell = cursor.fetchall()
    myanimals = []
    for animal in tosell:
        if animal['race'] == 'Kitteh':
            cursor.execute("SELECT pelage, castre, degriffe FROM cat WHERE id = {}".format(animal['id']))
        elif animal['race'] == 'Doggo':
            cursor.execute("SELECT pelage, castre, degriffe FROM dog WHERE id = {}".format(animal['id']))
        elif animal['race'] == 'Birb':
            cursor.execute("SELECT plumage FROM bird WHERE id = {}".format(animal['id']))
        race = cursor.fetchall()[0]
        myanimals.append({**animal, **race})
    return render_template('account-my-animals.html', tosell=myanimals)


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
    return render_template('contact_us.html')


@app.route('/account/preferences', methods=["GET", "POST"])
@login_required
def account_preferences():
    if request.method == "GET" and request.args.to_dict().get('Save') == "Save":
        updatePreferences(current_user, request.args.to_dict())
        print(current_user.preferencesCat)
        print(current_user.preferencesDog)
        print(current_user.preferencesBird)
    return render_template("account-preferences.html", prefCat=list(current_user.preferencesCat.keys()), prefDog=list(current_user.preferencesDog.keys()), prefBirb=list(current_user.preferencesBird.keys()))



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
def changeuser(field, new):
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
def changeuserimg(field, new):
    cursor = get_db()
    cursor.execute("UPDATE user SET {} = '{}' WHERE username = '{}'".format(field, new, current_user.username))
    return redirect(request.referrer)


@app.route("/animal/change/<ID>/<field>=<new>")
@login_required
def changeanimal(ID, field, new):
    cursor = get_db()
    cursor.execute("")
    return redirect(request.referrer)


@app.route('/animal/change/<ID>/image/<field>=<path:new>')
@login_required
def changeanimalimg(ID, field, new):
    cursor = get_db()
    cursor.execute("UPDATE pic SET {} = '{}' WHERE id = '{}'".format(field, new, ID))
    return redirect(request.referrer)


@app.route('/user/<username>')
@login_required
def username(username):
    cursor = get_db()
    cursor.execute(
        "SELECT U.username, U.nom, U.prenom, U.nom, U.email, U.profileImage, U.telephone FROM user U WHERE U.username = '{}'".format(
            username))
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

    #filter based on personal preferences
    possible_id = filterIds(possible_id)

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

        if animal['race'] == 'Doggo':
            if prefsDog['maleGenderDoggo'] and animal['sexe'] == 'm' or prefsDog['femaleGenderDoggo'] and animal['sexe'] == 'f':
                if prefsDog['0_20WeightDoggo'] and animal['poids'] <= 20 or prefsDog['20_40WeightDoggo'] and 20 < animal['poids'] <= 40 or prefsDog['40WeightPlusDoggo'] and animal['poids'] > 40:
                    if prefsDog['0_5AgeDoggo'] and animal['age'] <= 5 or prefsDog['5_10AgeDoggo'] and 5 < animal['age'] <= 10 or prefsDog['10AgePlusDoggo'] and animal['age'] > 10:
                        sql = "SELECT * FROM dog WHERE id={}"
                        cursor.execute(sql.format(animalId['id']))
                        dog = cursor.fetchall()[0]

                        if prefsDog['declawedDoggo'] == dog['degriffe'] and prefsDog['castratedDoggo'] == dog['castre']:
                            if prefsDog['gingerDoggo'] and dog['pelage'] == 'ginger' or prefsDog['whiteDoggo'] and dog['pelage'] == 'white' or prefsDog['blackDoggo'] and dog['pelage'] == 'black' or prefsDog['brownDoggo'] and dog['pelage'] == 'brown' or prefsDog['greyDoggo'] and dog['pelage'] == 'grey':
                                goodIds.append({'id': animalId['id']})

        elif animal['race'] == 'Kitteh':
            if prefsCat['maleGenderCat'] and animal['sexe'] == 'm' or prefsCat['femaleGenderCat'] and animal['sexe'] == 'f':
                if prefsCat['0_10WeightCat'] and animal['poids'] <= 10 or prefsCat['10_20WeightCat'] and 10 < animal['poids'] <= 20 or prefsCat['20PlusWeightCat'] and animal['poids'] > 20:
                    if prefsCat['0_5AgeCat'] and animal['age'] <= 5 or prefsCat['5_10AgeCat'] and 5 < animal['age'] <= 10 or prefsCat['10PlusAgeCat'] and animal['age'] > 10:
                        sql = "SELECT * FROM cat WHERE id={}"
                        cursor.execute(sql.format(animalId['id']))
                        cat = cursor.fetchall()[0]

                        if prefsCat['declawedCat'] == cat['degriffe'] and prefsCat['castratedCat'] == cat['castre']:
                            if prefsCat['gingerCat'] and cat['pelage'] == 'ginger' or prefsCat['whiteCat'] and cat['pelage'] == 'white' or prefsCat['blackCat'] and cat['pelage'] == 'black' or prefsCat['brownCat'] and cat['pelage'] == 'brown' or prefsCat['greyCat'] and cat['pelage'] == 'grey':
                                goodIds.append({'id': animalId['id']})

        elif animal['race'] == 'Birb':
            if prefsBirb['maleBirb'] and animal['sexe'] == 'm' or prefsBirb['femaleBirb'] and animal['sexe'] == 'f':
                if prefsBirb['0_1WeightBirb'] and animal['poids'] <= 1 or prefsBirb['1_2WeightBirb'] and 1 < animal['poids'] <= 2 or prefsBirb['2PlusWeightBirb'] and animal['poids'] > 3:
                    if prefsBirb['0_5AgeBirb'] and animal['age'] <= 5 or prefsBirb['5_10AgeBirb'] and 5 < animal['age'] <= 10 or prefsBirb['10AgePlusBirb'] and animal['age'] > 10:
                        sql = "SELECT * FROM bird WHERE id={}"
                        cursor.execute(sql.format(animalId['id']))
                        bird = cursor.fetchall()[0]

                        if prefsBirb['yellowBirb'] and bird['plumage'] == 'yellow' or prefsBirb['blackBirb'] and bird['plumage'] == 'black' or prefsBirb['whiteBirb'] and bird['plumage'] == 'white' or prefsBirb['greyBirb'] and bird['plumage'] == 'grey' or prefsBirb['greenBirb'] and bird['plumage'] == 'green' or prefsBirb['beigeBirb'] and bird['plumage'] == 'beige':
                            goodIds.append({'id': animalId['id']})
    return goodIds


if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(debug=True)
