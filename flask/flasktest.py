from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'a2f8836ec3c14d304d0422e18a0e4366' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

posts = [
    {
        'author' : 'Allison Arabelo',
        'title' : 'Job post',
        'content' : 'opening',
        'date_posted' : 'May 20, 1996'
    },
    
    {
        'author' : 'Zachary Chao',
        'title' : 'Job post',
        'content' : 'opening',
        'date_posted' : 'May 20, 1996'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!', 'success') #success is a bootstrap class
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'alliebaby@zach.com' and form.password.data == "asdlkj":
            flash('You have logged in.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title = 'Login', form = form)

if __name__ == '__main__':
	app.run(debug=True)