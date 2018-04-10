from datetime import timedelta
import pymysql
from flask import Flask, render_template, request, g, redirect, url_for
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

from Forms.LoginForm import LoginForm, RegisterForm
from Users import *
from persistance.passwordUtil import check_password

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY="plz giv boop and nuggers",
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
    if request.method == 'GET':
        return render_template('browse.html', data=data)
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


@app.route('/account-info')
@login_required
def account_info():
    return render_template('account-info.html')


@app.route("/", methods=["GET", "POST"])
def login_page():
    login_form = LoginForm(request.form)
    register_form = RegisterForm(request.form)

    if request.method == "POST":
        if login_form.validate_on_submit() and request.form['btn'] == "Login":
            user = User.get(login_form.email.data)

            if user and check_password(user.password, login_form.password.data):
                login_user(user, remember=True)
                cursor = get_db()
                sql = "SELECT * FROM user WHERE email='{}';"
                cursor.execute(sql.format(login_form.email.data))
                data = cursor.fetchall()

                return redirect(request.args.get("next") or url_for("browse", data=data))

            return render_template("home.html")
        if register_form.validate_on_submit() and request.form['btn'] == "Create":
            print("we wanna create an account")
            return render_template("about.html")

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


if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(debug=True)
