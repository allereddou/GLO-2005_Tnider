from datetime import timedelta
import pymysql
from flask import Flask, render_template, request, g, redirect, url_for
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import math, random

from Forms.LoginForm import LoginForm, RegisterForm
from Users import *
from persistance.bdUtils import createUser, checkIfUsernameAlreadyUsed, checkIfEmailAlreadyUsed, validatePassword

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY="plz giv boop and nuggers",
    REMEMBER_COOKIE_DURATION=timedelta(days=7)
))

login_manager = LoginManager()
login_serializer = URLSafeTimedSerializer(app.secret_key)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/browse', methods=['GET', 'POST'])
@login_required
def browse():
    wishlist = get_animals_desired()
    data = get_profile(current_user.email)
    ids = []
    for animal in wishlist:
        ids.append(animal['id'])
    first = random.choice(ids)
    if request.method == 'GET':
        print("GET")
        return render_template('browse.html', wishlist=wishlist, dispo=wishlist, data=data, first=first)
    if request.method == 'POST':
        return redirect(url_for('browse', data=data))


@app.route('/account')
@login_required
def sign_in():
    return render_template('account.html')


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/account-preferences')
@login_required
def account_preferences():
    return render_template('account-preferences.html')


@app.route('/account-transactions')
@login_required
def account_transactions():
    return render_template('account-transactions.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/account-info')
@login_required
def account_info():
    return render_template('account-info.html')


@app.route("/", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("browse"))
    login_form = LoginForm(request.form)
    register_form = RegisterForm(request.form)

    if request.method == "POST":
        if login_form.validate_on_submit() and request.form['btn'] == "Login":
            user = User.get(login_form.email.data)

            print(login_form.email.data)
            print(login_form.password.data)

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
                        register_form.last_name.data, register_form.first_name.data, register_form.phone_number.data, 0)

            createUser(user)
            login_user(user, remember=True)
            return redirect(request.args.get("next") or url_for("browse"))

    return render_template("home.html")


@app.route("/logout/")
def logout_page():
    logout_user()
    return redirect("/")


def get_db():
    if not hasattr(g, 'cursor'):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             autocommit=True)

        g.cursor = db.cursor(pymysql.cursors.DictCursor)
        g.cursor.execute("USE PROJET_BD")
    return g.cursor


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'cursor'):
        g.cursor.close()


@login_manager.user_loader
def load_user(email):
    return User.get(email)


@app.route("/restricted/")
@login_required
def restricted_page():
    user_id = (current_user.get_id() or "No User Logged In")
    return render_template("restricted.html", user_id=user_id)


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
            "SELECT DISTINCT A.id, P.link, A.nom, A.race, A.location FROM pic P, animal A WHERE A.id = P.id and A.id = {};".format(
                current_id['id']))
        animal = cursor.fetchall()
        wishlist.append(animal[0])
    for animal in wishlist:
        print(animal)
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


if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(debug=True)
