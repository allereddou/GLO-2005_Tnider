from datetime import timedelta
from flask import Flask, render_template, request, g, redirect, url_for
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from Forms.LoginForm import LoginForm, RegisterForm
from persistance.Users import *
from persistance.bdUtils import createUser, checkIfUsernameAlreadyUsed, checkIfEmailAlreadyUsed, validatePassword, \
    updatePreferences

from persistance.serverUtil import *

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


@app.route('/account/myanimals/<active>')
@login_required
def myanimals(active):
    myanimals = findMyAnimals(current_user)
    return render_template('account-my-animals.html', tosell=myanimals, active=active)


@app.route('/account/myanimals/trash/<num>')
@login_required
def trash(num):
    if deleteAnimalFromBD(num):
        return redirect(request.referrer)
    else:
        return redirect('404.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/browse', methods=['GET', 'POST'])
@login_required
def browse():
    global dispo
    wishlist = get_animals_desired(current_user)
    try:
        dispo = get_possible_match(current_user)
    except:
        dispo = {'id': 'none'}
    if request.method == 'GET':
        return render_template('browse.html', wishlist=wishlist, animal=dispo, first=dispo['id'])
    if request.method == 'POST':
        return render_template('browse.html', wishlist=wishlist, animal=dispo, first=dispo['id'])


@app.route('/browse/like')
@login_required
def like():
    likeAnimal(dispo['id'], current_user)
    return redirect(request.referrer)


@app.route('/browse/dislike')
@login_required
def dislike():
    dislikeAnimal(dispo['id'], current_user)
    return redirect(request.referrer)


@app.route('/deletenotdesired')
@login_required
def delete_not_desired():
    deleteNotDesiredinBD(current_user)
    return redirect(request.referrer)


@app.route('/browse/delete')
@login_required
def delete_desired():
    num = request.args['num']
    deleteDesiredinBD(num, current_user)
    return redirect(request.referrer)


@app.route('/browse/buy')
@login_required
def buy():
    num = request.args['num']
    buyAnimalAndCleanBD(num, current_user)
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
        pref = request.args.to_dict()
        updatePreferences(current_user, pref)
        return render_template("account-preferences.html", prefDog=current_user.preferencesDog,
                               prefCat=current_user.preferencesCat, prefBird=current_user.preferencesBird)
    return render_template("account-preferences.html", prefDog=current_user.preferencesDog,
                           prefCat=current_user.preferencesCat, prefBird=current_user.preferencesBird)


@app.route('/account/transactions')
@login_required
def account_transactions():
    transactions = getTransactions(current_user)
    return render_template('account-transactions.html', sold=transactions[0], bought=transactions[1])


@app.route('/account/info')
@login_required
def account_info():
    return render_template('account-info.html')


@app.route('/account/info/change/<field>=<new>')
@login_required
def changeuser(field, new):
    changeUserinBD(current_user, field, new)
    return redirect(request.referrer)


@app.route('/account/info/change/image/<field>=<path:new>')
@login_required
def changeuserimg(field, new):
    changeUserImginBD(current_user, field, new)
    return redirect(request.referrer)


@app.route("/animal/change/<ID>/<field>=<new>")
@login_required
def changeanimal(ID, field, new):
    if not isYourAnimal(ID, current_user):
        return redirect('/')
    changeAnimalinBD(ID, field, new)
    return redirect('account/myanimals/' + ID)


@app.route('/animal/change/<ID>/castre=<castre>&degriffe=<degriffe>')
@login_required
def changeanimalother(ID, castre, degriffe):
    if not isYourAnimal(ID, current_user):
        return redirect('/')
    changeAnimalOtherinBD(ID, castre, degriffe)
    return redirect('account/myanimals/' + ID)


@app.route('/animal/change/<ID>/image=<path:new>')
@login_required
def changeanimalimg(ID, new):
    if not isYourAnimal(ID, current_user):
        return redirect('/')
    changeAnimalImginBD(ID, new)
    return redirect('account/myanimals/' + ID)


@app.route('/user/<username>')
@login_required
def user(username):
    lookedForUser = getUser(username)
    return render_template('user.html', user=lookedForUser)


@app.route('/addAnimal', methods=["GET", "POST"])
@login_required
def add_Animal():
    if request.method == "POST":
        # On va chercher les arguments de l'URL pour les passer à la BD
        animalID = getAvailableID()
        user_name = current_user.username
        caption = "This is a test caption"
        nom = request.form['Name']
        age = int(request.form['Age'])
        sex = request.form['Sex']
        if sex == "1":
            sex = "m"
        elif sex == "2":
            sex = "f"
        poids = int(request.form['poids'])
        location = request.form['location']
        description = request.form['description']
        picLink = request.form['picture']
        prix = request.form['prix']
        if request.form['btn'] == "addDog":
            race = "Doggo"
            sousrace = request.form['sousrace']
            pelage = request.form['pelage']
            castre = request.form['castre']
            degriffe = request.form['degriffe']
            if castre == "1":
                castre = 1
            elif castre == "2":
                castre = 0
            if degriffe == "1":
                degriffe = 1
            elif degriffe == "2":
                degriffe = 0
            addDog(animalID, nom, sex, age, poids, location, race, description, pelage, castre, degriffe, sousrace)
        elif request.form['btn'] == "addCat":
            race = "Kitteh"
            sousrace = request.form['sousrace']
            pelage = request.form['pelage']
            castre = request.form['castre']
            degriffe = request.form['degriffe']
            if castre == "1":
                castre = 1
            elif castre == "2":
                castre = 0
            if degriffe == "1":
                degriffe = 1
            elif degriffe == "2":
                degriffe = 0
            addCat(animalID, nom, sex, age, poids, location, race, description, pelage, castre, degriffe, sousrace)
        elif request.form['btn'] == "addBird":
            race = "Birb"
            sousrace = request.form['sousrace']
            plumage = request.form['plumage']
            addBird(animalID, nom, sex, age, poids, location, race, description, plumage, sousrace)
        addAnimalinVend(user_name, animalID, prix)
        addAnimalinPic(animalID, caption, picLink)
        return redirect(url_for('browse'))

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
                        defaultProfileImage, defaultPrefBird, defaultPrefCat, defaultPrefDog)

            createUser(user)
            login_user(user, remember=True)
            return redirect(request.args.get("next") or url_for("browse"))

    return render_template("home.html")


@app.route("/logout/")
def logout_page():
    logout_user()
    return redirect("/")


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


if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(debug=True)
