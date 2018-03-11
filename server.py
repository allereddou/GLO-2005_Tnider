from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signIn')
def signIn():
    return render_template('signIn.html')


@app.route('/signUp')
def signUp():
    return render_template('signUp.html')



if __name__ == '__main__':
    app.run(debug=True)
