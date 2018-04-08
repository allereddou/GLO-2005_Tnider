from flask import Flask, render_template


app = Flask(__name__)

login_manager = LoginManager()




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


if __name__ == '__main__':
    app.run(debug=True)
