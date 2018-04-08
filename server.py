from flask import Flask, render_template, flash, request, redirect, g
from flask_login import LoginManager
from LoginForm import LoginForm
from User import User
import pymysql

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    # 1. Fetch against the database a user by `id`
    # 2. Create a new object of `User` class and return it.
    u = DBUsers.query.get(id)
    return User(u.name, u.id, u.active)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/browse')
def browse():
    return render_template('browse.html')


@app.route('/account')
def sign_in():
    return render_template('account.html')


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


def get_db():
    if not hasattr(g, 'cursor'):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root')

        g.cursor = db.cursor(pymysql.cursors.DictCursor)
    return g.cursor


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'cursor'):
        g.cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
    login_manager.init_app(app)
