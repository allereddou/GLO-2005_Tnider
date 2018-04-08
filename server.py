from flask import Flask, render_template, flash, request, g
from flask_login import LoginManager
from LoginForm import LoginForm
from Users import *
import pymysql

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='allo key'
))

login_manager = LoginManager()


#@app.route('/')
#def index():
 #   return render_template('home.html')


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


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    print(form.email)
    print(form.password)
    print(form.validate())
    if request.method == 'POST':
        user = User(form.email.data, form.password.data)
        if user.validateLogin():
            flash('Thanks for logging in')
            return render_template('browse.html', form=form)
    return render_template('home.html', form=form)


def get_db():
    if not hasattr(g, 'cursor'):
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             autocommit=True)

        g.cursor = db.cursor(pymysql.cursors.DictCursor)
        g.cursor.execute("USE PROJET_BD")
        print("Cursor generated \n")
    return g.cursor


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'cursor'):
        g.cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
    login_manager.init_app(app)
