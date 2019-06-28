from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'a2f8836ec3c14d304d0422e18a0e4366' 

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
def hello():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login")
def login():
    form = RegistrationForm()
    return render_template('login.html', title = 'Login', form = form)

if __name__ == '__main__':
	app.run(debug=True)