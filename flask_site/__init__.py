from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a2f8836ec3c14d304d0422e18a0e4366' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:l1pt0n@localhost:5432/omniApp'
db = SQLAlchemy(app)

from flask_site import routes