from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a2f8836ec3c14d304d0422e18a0e4366' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:l1pt0n@localhost:5432/omniApp'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flask_site import routes