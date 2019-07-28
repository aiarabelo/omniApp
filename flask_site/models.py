from datetime import datetime
from flask_site import db, login_manager
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData
from flask_login import UserMixin


engine = create_engine("postgresql://postgres:l1pt0n@localhost:5432/omniApp")

@login_manager.user_loader
def load_user(user_id):
    """
    FUNCTION: Reloads the user from the user ID in the session
    user_id: 
    Returns the username with that ID
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship(
        "Post", backref="author", lazy=True
    )  # uppercase because Post refers to the class

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}' )"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # user.id is lowercase because it refers to the column id

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
