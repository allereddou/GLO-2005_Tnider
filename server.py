from flask import Flask, render_template, flash, request, g, redirect, url_for
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from persistance.passwordUtil import hash_password, check_password
from Users import *
import pymysql
from itsdangerous import URLSafeTimedSerializer
from LoginForm import LoginForm
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY="allo key",
    REMEMBER_COOKIE_DURATION=timedelta(days=7)
))

login_manager = LoginManager()
login_serializer = URLSafeTimedSerializer(app.secret_key)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/browse', methods=['GET', 'POST'])
@login_required
def browse(data=None):
    wishlist = get_animals()

    if request.method == 'GET':
        print("GET")
        return render_template('browse.html', wishlist=wishlist, dispo=wishlist, data=data)
    if request.method == 'POST':
        print("POST")
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
    form = LoginForm(request.form)
    if request.method == "POST":
        user = User.get(form.email.data)
        # If we found a user based on username then compare that the submitted
        # password matches the password in the database.  The password is stored
        # is a slated hash format, so you must hash the password before comparing
        # it.

        if user and check_password(user.password, form.password.data):
            login_user(user, remember=True)
            cursor = get_db()
            sql = "SELECT * FROM user WHERE email='{}';"
            cursor.execute(sql.format(form.email.data))
            data = cursor.fetchall()

            return redirect(request.args.get("next") or url_for("browse", data=data))

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
        # print("Cursor generated \n")
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


def get_animals():
    cursor = get_db()
    cursor.execute(
        "SELECT B.id, P.link, A.nom, A.race, A.location FROM bird B, pic P, animal A WHERE B.id = P.id and B.id=A.id;")
    return cursor.fetchall()


if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(debug=True)
