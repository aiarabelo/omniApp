from flask import render_template, url_for, flash, redirect, request
from flask_site import app, db, bcrypt
from flask_site.forms import RegistrationForm, LoginForm
from flask_site.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author' : 'Allison Arabelo',
        'title' : 'Job post',
        'content' : 'opening',
        'date_posted' : 'May 20, 1996'
    },
    
    {
        'author' : 'Audrey Chao',
        'title' : 'Job post',
        'content' : 'opening',
        'date_posted' : 'May 20, 1996'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts, current_user=current_user)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    FUNCTION: Registers
    hashed.password: password that is in the database (hashed for security)
    form.password.data: password that the user entered in the form when registering
    form.email.data: email that the user entered in the form during registration
    Returns the registration page with the page title "Register"
    """
    if current_user.is_authenticated: 
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success') 
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    FUNCTION: Logs in
    user.password: password that is in the database (hashed)
    form.password.data: password that the user entered in the form when trying to login
    form.email.data: email that the user entered in the form during login
    form.remember.data: True or False (checked or unchecked), for when a user wants details to be remembered
    next_page: loads the next page when you login from a page that prompts you to login
    Returns The login page, with a title of "Login". Flashes "unsuccessful login" if wrong credentials.
    """
    print(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title = 'Account')